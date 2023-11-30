# Chainlink Jobs

Chainlink external adapters for accessing dClimate weather data on IPFS for smart parametric coverage solutions.

- [Weather Metrics Reporting](https://github.com/Arbol-Project/external-adapters/blob/main/jobs/dclimate-apiv4-polygon.toml) (dClimate-apiv4)
    - This Chainlink job allows a user to make a request for V4 geotemporal dClimate weather data on IPFS and return a desired aggregate numerical metric and associated unit.
    - Configs
        - Polygon: 
            - Job ID (externalJobID)              = `7678aeaa-5bfa-4811-b0a1-6b5a6f05069a`
            - Operator Address (contractAddress)  = `0x2621E9C0bc1975E74Ec465DF7357607E617C7FF9`
            - Chain ID (evmChainID)               = `137`
            - LINK Token Address                  = `0xb0897686c545045aFc77CF20eC7A532E3120E0F1`
        - Mumbai: 
            - Job ID (externalJobID)              = `b886eeae-31f7-46ac-898c-5b568a9a5503`
            - Operator Address (contractAddress)  = `0x59FA4e3Fd486E5798C8F8d884f0F65A51A5dFF43`
            - Chain ID (evmChainID)               = `80001`
            - LINK Token Address                  = `0x326C977E6efc84E512bB9C30f76E30c160eD06FB`
    - Inputs: 
        - `string request_url`: the request URL describing the dClimate data to fetch on IPFS. This request URL follows the same format as the API at `https://api.dclimate.net/` for V4 API requests but excludes the root domain (so request URL strings begin at `/apiv4/`). Importantly, V3 request URLs are no longer supported.
        - `string[] spatial_parameters`: the parameters for filtering the data spatially. 
        - `string[] temporal_parameters`: the parameters for aggregating the filtered data temporally. See `examples/SimpleParametricCoveragePolygon.sol` for all specifications.
    - Outputs:
        - `uint256 value`: the final value returned after aggregating the requested data. All numerical values that are not timestamps are multiplied by `1e18` and cast to integers before being returned on-chain.
        - `string unit`: the unit for the returned final value, if applicable. If the request fails, the adapter attempts to return an error message in the unit slot.

Explorer pages for Operator contracts:
- [Polygon](https://polygonscan.com/address/0x2621E9C0bc1975E74Ec465DF7357607E617C7FF9)
- [Mumbai](https://mumbai.polygonscan.com/address/0x59FA4e3Fd486E5798C8F8d884f0F65A51A5dFF43)
