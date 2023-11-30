// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";

contract SimpleV4ParametricMumbai is ChainlinkClient {
    using Chainlink for Chainlink.Request;

    uint256 private constant ORACLE_PAYMENT = 1 * 10**10; // 0.00000001 LINK
    address constant LINK_ADDRESS = 0x326C977E6efc84E512bB9C30f76E30c160eD06FB; // <- Mumbai, Polygon -> 0xb0897686c545045aFc77CF20eC7A532E3120E0F1
    address constant CHAINLINK_OPERATOR_ADDRESS = 0x59FA4e3Fd486E5798C8F8d884f0F65A51A5dFF43; // <- Mumbai, Polygon -> 0x2621E9C0bc1975E74Ec465DF7357607E617C7FF9
    bytes32 constant CHAINLINK_JOB_ID = "b886eeae31f746ac898c5b568a9a5503"; // <- Mumbai, Polygon -> "7678aeaa5bfa4811b0a16b5a6f05069a"

    // v4 geotemporal query for rainfall data outputted to an array
    string request_URL = "/geo_temporal_query/chirpsc_final_25-daily?output_format=array";
    /**
     * Spatial Parameters
     * point_params : (lat: float, lon: float)
     * circle_params : (center_lat: float, center_lon: float, radius: float) # radius in KM
     * rectangle_params : (min_lat: float, min_lon: float, max_lat: float, max_lon: float)
     * polygon_params : (epsg_crs: int)
     * multiple_points_params : (epsg_crs: int)
     * spatial_agg_params : (agg_method: str)
     * 
     * Example parameters for single point query
     */
    string[] spatial_parameters = ["point_params", "13.34126091", "103.39190674"];
    /**
     * Temporal Parameters
     * time_range : [start_time: str, end_time: str] # datetimes in ISO Format structured as list with two elements
     * temporal_agg_params : (time_period: str, agg_method: str, time_unit: int)
     * rolling_agg_params : (window_size: int, agg_method: str)
     *
     * Example parameters for summing data over a specific time period
     */
    string[] temporal_parameters = ["time_range", "2022-09-01", "2022-09-30", "temporal_agg_params", "all", "sum"];

    uint256 public data;
    string public unit;

    constructor()
    {
        setChainlinkToken(LINK_ADDRESS);
    }

    function sendRequest()
        public
    {
        Chainlink.Request memory req = buildChainlinkRequest(CHAINLINK_JOB_ID, address(this), this.fulfillRequest.selector);
        req.add("request_url", request_URL);
        req.addStringArray("spatial_parameters", spatial_parameters);
        req.addStringArray("temporal_parameters", temporal_parameters);
        sendChainlinkRequestTo(CHAINLINK_OPERATOR_ADDRESS, req, ORACLE_PAYMENT);
    }

    /**
     * @dev Callback function for chainlink oracle requests
     * numberical results multiplied by 1e18 and cast to integer
     */
    function fulfillRequest(bytes32 _requestId, uint256 _result, string memory _unit)
        public
        recordChainlinkFulfillment(_requestId)
    {
        uint someThreshold;
        data = _result;
        unit = _unit;
        if (data > someThreshold) {
            doSomething();
        }
    }

    // do something with the parametric result
    function doSomething() private {}
}
