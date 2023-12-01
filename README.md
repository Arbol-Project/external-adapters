# Arbol External Adapters

This repository features external adapters, Chainlink jobs, and example smart contracts for requesting and operating on dClimate weather data over IPFS to provide oracle solutions for on-chain parametric products. 

On-Chain Addresses
- Polygon: chain ID (evmChainID) `137`
    - Operator Address (contractAddress)  = `0x2621E9C0bc1975E74Ec465DF7357607E617C7FF9`
    - LINK Token Address                  = `0xb0897686c545045aFc77CF20eC7A532E3120E0F1`
- Mumbai: chain ID (evmChainID) `80001`
    - Operator Address (contractAddress)  = `0x59FA4e3Fd486E5798C8F8d884f0F65A51A5dFF43`
    - LINK Token Address                  = `0x326C977E6efc84E512bB9C30f76E30c160eD06FB`

[Weather Metrics Reporting Jobs](https://github.com/Arbol-Project/external-adapters/blob/main/jobs/)
- Version: `v4`
    - Job IDs (externalJobID): 
        - Polygon: `7678aeaa-5bfa-4811-b0a1-6b5a6f05069a`
        - Mumbai: `b886eeae-31f7-46ac-898c-5b568a9a5503`
    - Query Types: 
        - `geo_temporal_query`
            - Inputs:
                - `string request_url`: the request URL following the format for API requests to `https://api.dclimate.net/` but excluding the root domain
                    - Header Parameters:
                        - `dataset_name`: name of geotemporal dataset, accepts values from `[agb-quarterly, chirps_final_05-daily, chirps_final_25-daily, chirps_prelim_05-daily, copernicus_ocean_salinity_0p5_meters-daily, copernicus_ocean_salinity_109_meters-daily, copernicus_ocean_salinity_1p5_meters-daily, copernicus_ocean_salinity_25_meters-daily, copernicus_ocean_salinity_2p6_meters-daily, copernicus_ocean_sea_level-daily, copernicus_ocean_temp_1p5_meters-daily, copernicus_ocean_temp_6p5_meters-daily, cpc_precip_global-daily, cpc_precip_us-daily, cpc_temp_max-daily, cpc_temp_min-daily, deforestation-quarterly, era5_2m_temp-hourly, era5_land_precip-hourly, era5_land_surface_pressure-hourly, era5_precip-hourly, era5_surface_solar_radiation_downwards-hourly, era5_wind_100m_u-hourly, era5_wind_100m_v-hourly, era5_wind_10m_u-hourly, era5_wind_10m_v-hourly, prism-precip-daily, prism-tmax-daily, prism-tmin-daily, vhi-weekly,]`
                        - `desired_format`: desired output format, accepts values from `[array,]`
                    - Format: `"/apiv4/geo_temporal_query/<dataset_name>?output_format=<desired_format>"`
                    - Example: `string request_URL = "/apiv4/geo_temporal_query/chirps_final_25-daily?output_format=array";`
                - `string[] spatial_parameters`: parameters for spatial filtering, requires that the first element be one of the following spatial filters and the remaining elements be the associated input values (in displayed order). All spatial units are in degrees of latitude/longitude unless otherwise specified. The `epsg_crs` for `polygon_params` and `multiple_points_params` refers to the Coordinate Reference System (projection) of the dataset. It defaults to 4326 (WGS84), or recommended projection. 
                    - Spatial Filters:
                        - `point_params` : `(lat: float, lon: float)`
                        - `circle_params` : `(center_lat: float, center_lon: float, radius: float)` # radius in `km`
                        - `rectangle_params` : `(min_lat: float, min_lon: float, max_lat: float, max_lon: float)`
                        - `polygon_params` : `(epsg_crs: int)`
                        - `multiple_points_params` : `(epsg_crs: int)`
                        - `spatial_agg_params` : `(agg_method: str)`
                    - Format: `[<spatial_filter_name>, <filter_input_1>, <filter_input_2>,...]`
                    - Example: `string[] spatial_parameters = ["point_params", "1.375", "103.39190674"];`
                - `string[] temporal_parameters`: parameters for temporal filtering and aggregation, requires that the first three elements define the time range for the requested data followed by one of the temporal aggregators defined below and the associated input values (in displayed order). Valid aggregation methods for all agg requests are `min`, `max`, `median`, `mean`, `std`, and `sum`. Only one may be specified in a given set of parameters. 
                    - `time_range` : `[start_time: str, end_time: str]` # in ISO Format
                    - Temporal Aggregators:
                        - `temporal_agg_params` : `(time_period: str, agg_method: str, time_unit: int)`
                            - Valid time periods for are `hour`, `day`, `week`, `month`, `quarter`, `year`, and `all`. Only one may be specified in a given set of parameters.
                            - `time_unit` refers to the number of time periods to aggregate by. It defaults to `1`.
                        - `rolling_agg_params` : `(window_size: int, agg_method: str)`
                            - `window_size` refers to the number of units of time used to construct the rolling aggregation. The specific unit depends on the dataset.​
                    - Format: `["time_range", <start_time>, <end_time>, <temporal_agg_name>, <agg_input_1>, <agg_input_2>,...]`
                    - Example: `string[] temporal_parameters = ["time_range", "2022-09-01", "2022-09-30", "temporal_agg_params", "all", "max", "1"];`
            - Outputs:
                - `uint64 value`: the final value returned after aggregating the requested data. All numerical values that are not timestamps are multiplied by `1e18` and cast to `uint64` before being returned on-chain.
                - `string memory unit`: the unit for the returned final value, if applicable. If the request fails, the adapter attempts to return an error message in the unit slot.
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
