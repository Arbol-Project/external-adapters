# Arbol External Adapters

This repository features external adapters, Chainlink jobs, and example smart contracts for requesting and operating on dClimate weather data over IPFS to provide oracle solutions for on-chain parametric products

On-Chain Addresses
- **Polygon**: chain ID (evmChainID) `137`
    - Operator Address (contractAddress)  = `0x2621E9C0bc1975E74Ec465DF7357607E617C7FF9`
    - LINK Token Address                  = `0xb0897686c545045aFc77CF20eC7A532E3120E0F1`
- **Mumbai**: chain ID (evmChainID) `80001`
    - Operator Address (contractAddress)  = `0x59FA4e3Fd486E5798C8F8d884f0F65A51A5dFF43`
    - LINK Token Address                  = `0x326C977E6efc84E512bB9C30f76E30c160eD06FB`

[Weather Metrics Reporting Jobs](https://github.com/Arbol-Project/external-adapters/blob/main/jobs/)
- Version: `v3`
    - Job IDs (externalJobID):
        - **Polygon**: `80062f57-3ef7-4d06-b370-c52886dc2d8b`
        - **Mumbai**: `cb30734b-90b0-44d9-82b8-f5a1d63faf7e`
    - Inputs:
        - `string request_url`: the request URL following the format for API requests to `https://api.dclimate.net/` but excluding the root domain. See supported request endpoints below
        - `string[] request_ops`: the request operations as a list of strings matching [Pandas.Series](https://pandas.pydata.org/docs/reference/series.html) or [Pandas.DataFrame](https://pandas.pydata.org/docs/reference/frame.html) methods to be used on the requested data to produce a single output for writing back to chain
            - Format: `[<op_1>, <op_2>,...]`
            - Example: `["last", "min"]`
        - `string[] request_params`: the request parameters as a list of strings representing arguments for applying requested operations. Each method in `request_ops` should have a corresponding formatted string in `request_params` containing a list of arguments for the method. The results of applying a method to the retrieved data will be used as the input to the next method in the list
            - Format: `["[<op_1_arg_1>, <op_1_arg_2>,...]","[<op_2_arg_1>,...]"...]`
            - Example: `["['1M']", "[]"]`
    - Outputs:
        - `uint64 value`: the final value returned performing the requested operations on the retrieved data. All numerical values that are not timestamps are multiplied by `1e18` and cast to `uint64` before being returned on-chain
        - `string memory unit`: the unit for the returned final value, if applicable. If the request fails, the adapter attempts to return an error message in the unit slot
    - Request URLs:
        - Endpoint: `australia-station-history`
            - Format: `"/apiv3/australia-station-history/{station_name}/{weather_variable}?desired_units=<desired_units>&as_of=<as_of>"`
            - URL Parameters:
                - `station_name`: name of station, accepts values from `enums.australia-station-history.txt`
                - `weather_variable`: weather variable to get data for, accepts values from `["TMAX","TMIN","PRCP","GUSTSPEED","GUSTDIR"]`
            - Optional URL Arguments:
                - `desired_units`: desired units to convert the output to, defaults to `None` (i.e. default dataset units)
                - `as_of`: an ISO formatted date representing the version of the data to use, defaults to `None` (i.e. current)
            - Example: `string request_URL = "/apiv3/australia-station-history/Brisbane/TMAX";`
        <!-- - `cme-futures` -->
        <!-- - `cme-history` -->
        <!-- - `cwv-station-history` -->
        - Endpoint: `dutch-station-history`
            - Format: `"/apiv3/dutch-station-history/{station_name}/{weather_variable}?use_imperial_units=<use_imperial_units>&desired_units=<desired_units>"`
            - URL Parameters:
                - `station_name`: number of station, accepts values from `enums.dutch-station-history.txt`
                - `weather_variable`: weather variable to get data for, accepts values from `["WINDSPEED","RADIATION","TMAX","TMIN","TAVG"]`
            - Optional URL Arguments:
                - `use_imperial_units`: whether to use imperial or metric units, defaults to `True`
                - `desired_units`: desired units to convert the output to, defaults to `None` (i.e. default dataset units)
            - Example: `string request_URL = "/apiv3/dutch-station-history/210/WINDSPEED?use_imperial_units=true";`
        <!-- - `eaufrance` -->
        <!-- - `forecasts` -->
        <!-- - `german-station-history` -->
        <!-- - `german-station-hourly-history` -->
        <!-- - `ghcn-history` -->
        <!-- - `ghisd-station-history` -->
        - Endpoint: `grid-history`
            - Format: `"/apiv3/grid-history/{dataset}/{lat}_{lon}?use_imperial_units=<use_imperial_units>&desired_units=<desired_units>&convert_to_local_time=<convert_to_local_time>&as_of=<as_of>"`
            - URL Parameters:
                - `dataset`: name of gridded dataset, accepts values from `enums.grid-history.txt`
                - `lat`: latitude of desired data, float
                - `lon`: longitude of desired data, float
            - Optional URL Arguments:
                - `use_imperial_units`: whether to use imperial or metric units, defaults to `True`
                - `desired_units`: desired units to convert the output to, defaults to `None` (i.e. default dataset units)
                - `convert_to_local_time`: whether to convert results to local timezone, defaults to `True`
                - `as_of`: an ISO formatted date representing the version of the data to use, defaults to `None` (i.e. current)
            - Example: `string request_URL = "/apiv3/grid-history/era5_land_precip-hourly/1.375_103.875?use_imperial_units=true&convert_to_local_time=true";`
        <!-- - `inmet` -->
        <!-- - `japan-station-history` -->
        <!-- - `power-history/ne_iso/load` -->
        <!-- - `storms` -->
        <!-- - `teleconnections` -->
        <!-- - `uk-national-grid/sap` -->
- Version: `v4`
    - Job IDs (externalJobID): 
        - **Polygon**: `7678aeaa-5bfa-4811-b0a1-6b5a6f05069a`
        - **Mumbai**: `b886eeae-31f7-46ac-898c-5b568a9a5503`
    - Inputs:
        - `string request_url`: the request URL following the format for API requests to `https://api.dclimate.net/` but excluding the root domain. See supported request endpoints below
        - `string[] spatial_parameters`: parameters for spatial filtering, requires that the first element be one of the Spatial Filters below and the remaining elements be the associated input values (in displayed order). All spatial units are in degrees of latitude/longitude unless otherwise specified. The `epsg_crs` for `polygon_params` and `multiple_points_params` refers to the Coordinate Reference System (projection) of the dataset. It defaults to 4326 (WGS84), or recommended projection 
            - Format: `[<spatial_filter_name>, <filter_input_1>, <filter_input_2>,...]`
            - Spatial Filters:
                - `point_params` : `(lat: float, lon: float)`
                - `circle_params` : `(center_lat: float, center_lon: float, radius: float)` # radius in `km`
                - `rectangle_params` : `(min_lat: float, min_lon: float, max_lat: float, max_lon: float)`
                - `polygon_params` : `(epsg_crs: int)`
                - `multiple_points_params` : `(epsg_crs: int)`
                - `spatial_agg_params` : `(agg_method: str)`
            - Example: `string[] spatial_parameters = ["point_params", "1.375", "103.39190674"];`
        - `string[] temporal_parameters`: parameters for temporal filtering and aggregation, requires that the first two elements define the start and end of the time range (in ISO format) for the requested data followed by one of the Temporal Aggregators below and the associated input values (in displayed order). Valid aggregation methods for all agg requests are `min`, `max`, `median`, `mean`, `std`, and `sum`. Only one may be specified in a given set of parameters
            - Format: `[<start_time>, <end_time>, <temporal_agg_name>, <agg_input_1>, <agg_input_2>,...]`
            - Temporal Aggregators:
                - `temporal_agg_params` : `(time_period: str, agg_method: str, time_unit: int)`
                    - Valid time periods for are `hour`, `day`, `week`, `month`, `quarter`, `year`, and `all`. Only one may be specified in a given set of parameters.
                    - `time_unit` refers to the number of time periods to aggregate by. It defaults to `1`
                - `rolling_agg_params` : `(window_size: int, agg_method: str)`
                    - `window_size` refers to the number of units of time used to construct the rolling aggregation. The specific unit depends on the dataset
            - Example: `string[] temporal_parameters = ["time_range", "2022-09-01", "2022-09-30", "temporal_agg_params", "all", "max", "1"];`
    - Outputs:
        - `uint64 value`: the final value returned after aggregating the requested data. All numerical values that are not timestamps are multiplied by `1e18` and cast to `uint64` before being returned on-chain
        - `string memory unit`: the unit for the returned final value, if applicable. If the request fails, the adapter attempts to return an error message in the unit slot
    - Request URLs:
        - Endpoint: `geo_temporal_query`
            - Format: `"/apiv4/geo_temporal_query/{dataset}?output_format=<output_format>"`
            - URL Parameters:
                - `dataset`: name of geotemporal dataset, accepts values from `enums.geo_temporal_query.txt`
            - Optional URL Arguments:
                - `output_format`: desired output format, accepts values from `[array]`, defaults to `array`
            - Example: `string request_URL = "/apiv4/geo_temporal_query/chirps_final_25-daily?output_format=array";`
        - Types of invalid requests include:
            - Specifying too many points or too large areas
            - Specifying multiple geographic filters (e.g. polygon AND circle)
            - Specifying temporal and rolling time-based aggregations
            - Providing shapefiles with invalid geometries or projections
            - Selecting an area/time period with all null data
            - Requesting invalid output formats (or just misspelling them)​

Explorer pages for Operator contracts:
- [Polygon](https://polygonscan.com/address/0x2621E9C0bc1975E74Ec465DF7357607E617C7FF9)
- [Mumbai](https://mumbai.polygonscan.com/address/0x59FA4e3Fd486E5798C8F8d884f0F65A51A5dFF43)
