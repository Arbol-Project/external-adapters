// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";

contract SimpleV3ParametricPolygon is ChainlinkClient {
    using Chainlink for Chainlink.Request;

    // IMPORTANT: after deploying, must send required oracle payment to this example contract before calling sendRequest()
    uint256 private constant ORACLE_PAYMENT = 1 * 10**16; // 0.01 LINK
    address constant LINK_ADDRESS = 0xb0897686c545045aFc77CF20eC7A532E3120E0F1; // <- Polygon, Mumbai -> 0x326C977E6efc84E512bB9C30f76E30c160eD06FB
    address constant CHAINLINK_OPERATOR_ADDRESS = 0x2621E9C0bc1975E74Ec465DF7357607E617C7FF9; // <- Polygon, Mumbai -> 0x59FA4e3Fd486E5798C8F8d884f0F65A51A5dFF43
    bytes32 constant CHAINLINK_JOB_ID = "80062f573ef74d06b370c52886dc2d8b"; // <- Polygon, Mumbai -> "cb30734b90b044d982b8f5a1d63faf7e"

    string request_URL = "/apiv3/dutch-station-history/210/WINDSPEED?use_imperial_units=true";
    string[] request_ops = ["last", "max"];
    string[] request_params = ["['1M']", "[]"];

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
        req.addStringArray("request_ops", request_ops);
        req.addStringArray("request_params", request_params);
        sendChainlinkRequestTo(CHAINLINK_OPERATOR_ADDRESS, req, ORACLE_PAYMENT);
    }

    /**
     * @dev Callback function for chainlink oracle requests
     * numberical results multiplied by 1e18 and cast to integer
     */
    function fulfillRequest(bytes32 _requestId,  uint64 _value, string memory _unit)
        public
        recordChainlinkFulfillment(_requestId)
    {
        uint someThreshold;
        data = uint256(_value);
        unit = _unit;
        if (data > someThreshold) {
            doSomething();
        }
    }

    function resetData()
        public
    {
        data = 0;
        unit = "";
    }

    // do something with the parametric result
    function doSomething() private {}
}
