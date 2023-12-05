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
        - `string request_url`: the request URL following the format for API requests to `https://api.dclimate.net/` but excluding the root domain. See supported request types below
        - `string[] request_ops`: the request operations as a list of strings matching [Pandas.Series](https://pandas.pydata.org/docs/reference/series.html) or [Pandas.DataFrame](https://pandas.pydata.org/docs/reference/frame.html) methods to be used on the requested data to produce a single output for writing back to chain
            - Format: `[<op_1>, <op_2>,...]`
            - Example: `["last", "min"]`
        - `string[] request_params`: the request parameters as a list of strings representing arguments for applying requested operations. Each method in `request_ops` should have a corresponding formatted string in `request_params` containing a list of arguments for the method. The results of applying a method to the retrieved data will be used as the input to the next method in the list
            - Format: `["[<op_1_arg_1>, <op_1_arg_2>,...]","[<op_2_arg_1>,...]"...]`
            - Example: `["['1M']", "[]"]`
    - Outputs:
        - `uint64 value`: the final value returned performing the requested operations on the retrieved data. All numerical values that are not timestamps are multiplied by `1e18` and cast to `uint64` before being returned on-chain
        - `string memory unit`: the unit for the returned final value, if applicable. If the request fails, the adapter attempts to return an error message in the unit slot
    <!-- - `cme-futures` -->
    - Request Type: `australia-station-history`
        - Request URL:
            - Format: `"/apiv3/australia-station-history/<station_name>/<weather_variable>?desired_units=<desired_units>&as_of=<as_of>"`
            - URL Parameters:
                - `station_name`: name of geotemporal dataset, accepts values from `['Adelaide_Airport', 'Adelaide_West_Terrace___ngayirdapira', 'Adele_Island', 'Aireys_Inlet', 'Albany_Airport', 'Albion_Park', 'Albury', 'Alice_Springs_Airport', 'Alva_Beach', 'Amberley', 'Applethorpe', 'Archerfield', 'Argyle', 'Arlington_Reef', 'Armidale_Airport', 'Avalon', 'Ayr', 'Badgerys_Creek', 'Badgingarra', 'Bairnsdale', 'Ballarat', 'Ballera', 'Ballina', 'Bankstown', 'Barrow_Island', 'Batchelor', 'Bathurst_Airport', 'Beaudesert_AWS', 'Bedout_Island', 'Beerburrum', 'Bega', 'Bellambi', 'Ben_Nevis', 'Bendigo', 'Bickley', 'Biloela', 'Birdsville', 'Blackall', 'Blackwater_Airport', 'Bombala_AWS', 'Borroloola', 'Borrona_Downs', 'Bourke', 'Bowen_Airport_AWS', 'Bradshaw', 'BradshawAngallari_Valley_Defence', 'BradshawKoolendong_Valley', 'Braidwood', 'Brewon', 'Bridgetown', 'Brisbane', 'Brisbane_Airport', 'Broken_Hill_Airport', 'Broome', 'Bulman', 'Bunbury', 'Bundaberg', 'Burketown_Airport', 'Bushy_Park', 'Busselton_Airport', 'Busselton_Jetty', 'Butlers_Gorge', 'Cabramurra', 'Cairns', 'Cairns_Racecourse', 'Camden', 'Camooweal', 'Campania', 'Campbelltown', 'Canberra', 'Canterbury', 'Canungra_Defence', 'Cape_Borda', 'Cape_Bruny_AWS', 'Cape_Byron', 'Cape_Flattery', 'Cape_Grim', 'Cape_Jaffa', 'Cape_Leeuwin', 'Cape_Moreton', 'Cape_Naturaliste', 'Cape_Nelson', 'Cape_Otway', 'Cape_Sorell', 'Cape_Wessel', 'Cape_Willoughby', 'Carnarvon', 'Carters_Bore', 'Casino', 'Casterton', 'Ceduna', 'Central_Arnhem_Plateau', 'Centre_Island', 'Century_Mine', 'Cerberus', 'Cessnock_Airport', 'Charleville', 'Charlton', 'Christmas_Island', 'Clare', 'Clermont_Airport', 'Cleve_Airport', 'Cloncurry', 'Cobar', 'Cobar_Airport', 'Coconut_Island', 'Cocos_Island', 'Coen_Airport', 'Coffs_Harbour_Airport', 'Coldstream', 'Collie_East', 'Combienbar', 'Condobolin_Airport', 'Coober_Pedy_Airport', 'Cooktown', 'Coolangatta', 'Cooma_Airport', 'Coonabarabran_Airport', 'Coonamble', 'Coonawarra', 'Cowra', 'Cressy', 'Croker_Island_Airport', 'Cultana_Defence', 'Cummins_Airport', 'Cunderdin_Airport', 'Curtin', 'Dalby', 'Dalwallinu', 'Daly_Waters', 'Dartmoor', 'Darwin_Airport', 'Delamere', 'Delta', 'Deniliquin', 'Dennes_Point', 'Derby', 'Devonport_Airport', 'Double_Island_Point', 'Douglas_River', 'Dubbo', 'Dunalley', 'Dwellingup', 'East_Sale_Airport', 'Edenhope', 'Edinburgh', 'Edithburgh', 'Eildon_Fire_Tower', 'Emerald', 'ErnabellaPukatja', 'Esperance', 'Esperance_Airport', 'Essendon_Airport', 'Evans_Head', 'Falls_Creek', 'Fawkner_Beacon', 'Ferny_Creek', 'Fitzroy_Crossing', 'Flinders_Island_Airport', 'Flinders_Reef', 'Forbes', 'Forrest', 'Fowlers_Gap', 'Frankston_Ballam_Park', 'Frankston_Beach', 'Frederick_Reef', 'Friendly_Beaches', 'Gabo_Island', 'Garden_Island', 'Gayndah', 'Geelong_Racecourse', 'Gelantipy', 'Georgetown_Airport', 'Geraldton_Airport', 'Giles', 'Gingin_Airport', 'Girilambone', 'Gladstone', 'Gladstone_Airport', 'Glen_Innes_Airport', 'Gold_Coast_Seaway', 'Gooseberry_Hill', 'Gosford', 'Goulburn_Airport', 'Gove_Airport', 'Grafton_AgRS', 'Grafton_Airport', 'Green_Cape', 'Griffith', 'Groote_Eylandt_Airport', 'Grove', 'Gunnedah_Airport', 'Gympie', 'Halls_Creek', 'Hamilton', 'Hamilton_Island', 'Hartz_Mountains', 'Hay_Airport', 'Heron_Island', 'Hervey_Bay', 'Hindmarsh_Island', 'Hobart', 'Hobart_Airport', 'Hogan_Island', 'Holmes_Reef', 'Holsworthy', 'Holsworthy_Defence', 'Hopetoun_Airport', 'Hopetoun_North', 'Horn_Island', 'Horsham', 'Horsley_Park', 'Hughenden', 'Hunters_Hill', 'Inner_Beacon', 'Innisfail_Aero', 'Inverell_RS', 'Ivanhoe_Airport', 'Jabiru', 'Jacup', 'Jandakot', 'Jervis_Bay_Airfield', 'Jervois', 'Julia_Creek', 'Kadina', 'KalgoorlieBoulder', 'Kalumburu', 'Kanagulk', 'Kangaroo_Flats_Defence', 'Kapooka_Defence', 'Karijini_North', 'Karratha', 'Katanning_RS', 'Keith_West', 'Kempsey_Airport', 'Khancoban', 'Kiama', 'Kilmore_Gap', 'King_Island_Airport', 'Kingaroy', 'Kingscote', 'Kowanyama', 'Kuitpo', 'Kununurra_Airport', 'Kurnell', 'Kyabram', 'Lady_Elliot_Island', 'Lajamanu', 'Lake_Grace', 'Lake_Julius', 'Lake_Macquarie__Cooranbong', 'Lameroo_AWS', 'Lancelin_Defence', 'Larapuna_Eddystone_Point', 'Latrobe_Valley', 'Launceston', 'Launceston_Airport', 'Laverton', 'Learmonth', 'Legendre_Island', 'Leigh_Creek', 'Leinster', 'Leonora_Airport', 'Liawenee', 'Lihou_Reef_Lighthouse', 'Little_Bay', 'Lochington', 'Lockhart_River', 'Longerenong', 'Longreach', 'Lord_Howe_Island', 'Lord_Howe_Island_Windy_Point', 'Low_Head', 'Low_Isles', 'Low_Rocky_Point', 'Loxton', 'Lucinda', 'Luncheon_Hill', 'Maatsuyker_Island', 'Mackay', 'Mackay_Airport', 'Mackay_Racecourse', 'Macquarie_Island', 'Maitland_Airport', 'Mallacoota', 'Mandora', 'Mandurah', 'Mangalore', 'Mangrove_Mountain', 'Maningrida_Airport', 'Manjimup', 'Marble_Bar', 'Mareeba', 'Maria_Island', 'Marrangaroo_Defence', 'Marree_Airport', 'McArthur_River_Mine', 'McCluer_Island', 'Meekatharra', 'Melbourne_Airport', 'Melbourne_Olympic_Park', 'Melville_Water', 'Merimbula', 'Merriwa', 'Middle_Point', 'Mildura', 'Miles', 'Millendon_Swan_Valley', 'Minlaton_Airport', 'Minnipa_RS', 'Montague_Island', 'Moomba_Airport', 'Moorabbin_Airport', 'Moranbah_Airport', 'Morawa_Airport', 'Moree', 'Mornington_Island_Airport', 'Mortlake', 'Moruya_Airport', 'Moss_Vale', 'Mount_Baw_Baw', 'Mount_Boyce', 'Mount_Buller', 'Mount_Bundey_North_Defence', 'Mount_Crawford', 'Mount_Gambier', 'Mount_Gellibrand', 'Mount_Ginini', 'Mount_Hope', 'Mount_Hotham', 'Mount_Hotham_Airport', 'Mount_Isa', 'Mount_Lofty', 'Mount_Magnet_Airport', 'Mount_Moornapa', 'Mount_Nowa_Nowa', 'Mount_Read', 'Mount_Stuart_Defence', 'Mount_William', 'Mudgee', 'Munglinup_West', 'Murganella_Airstrip', 'Murrurundi_Gap', 'Nambour', 'Naracoorte', 'Narrabri', 'Narrandera_Airport', 'Neptune_Island', 'Nerriga', 'New_May_Downs', 'Newcastle_Nobbys', 'Newdegate', 'Newman_Airport', 'Ngukurr_AWS', 'Nhill_Aerodrome', 'Noarlunga', 'Noona', 'Noonamah', 'Norah_Head', 'Norfolk_Island', 'Normanton', 'Norseman_Airport', 'North_Head', 'North_Island', 'Nowra', 'Nullarbor', 'Nuriootpa', 'Oakey', 'Ocean_Reef', 'Omeo', 'Onslow_Airport', 'Oodnadatta', 'Orange_Airport', 'Orbost', 'Ouse', 'Padthaway', 'Pallamana', 'Palmerville', 'Paraburdoo', 'Parafield', 'Parawa_West', 'Parkes_Airport', 'Parndana', 'Pearce', 'Penrith', 'Perisher_Valley', 'Perth', 'Perth_Airport', 'Pirlangimpi', 'Point_Avoid', 'Point_Fawcett', 'Point_Perpendicular', 'Point_Stuart', 'Port_Augusta', 'Port_Fairy', 'Port_Hedland', 'Port_Macquarie_Airport', 'Portland_Airport', 'Pound_Creek', 'Proserpine', 'PuckapunyalLyon_Hill_Defence', 'Puckapunyal_West_Defence', 'Rabbit_Flat', 'Red_Rocks_Point', 'Redcliffe', 'Redesdale', 'Redland_Alexandra_Hills', 'Renmark_Airport', 'Rhyll', 'Richmond', 'Robe_Airport', 'Rockhampton', 'Rocky_Gully_South', 'Roebourne_Airport', 'Rolleston_Airport', 'Roma', 'Roseworthy', 'Rottnest_Island', 'Rowley_Shoals', 'Roxby_Downs', 'Rundle_Island', 'Rutherglen', 'Salmon_Gums_RS', 'Samuel_Hill', 'Scherger', 'Scone_Airport', 'Scoresby', 'Scotts_Peak', 'Scottsdale', 'Sellicks_Hill', 'Shannon', 'Shark_Bay_Airport', 'Sheffield', 'Sheoaks', 'Shepparton', 'Smithton', 'Smithville', 'Snowtown', 'South_Channel_Island', 'South_Johnstone', 'Southern_Cross_Airport', 'St_George', 'St_Helens', 'St_Kilda_Harbour_RMYS', 'St_Lawrence', 'Stawell', 'Stenhouse_Bay', 'Strahan', 'Strathalbyn', 'Sunshine_Coast_Airport', 'Swan_Hill', 'Swan_Island', 'Swanbourne', 'Sydney_Airport', 'Sydney_Harbour', 'Sydney_Olympic_Park', 'Sydney__Observatory_Hill', 'Tamworth_Airport', 'Tarcoola', 'Taree_Airport', 'Tasman_Island', 'Tatura', 'Telfer', 'Temora', 'Tennant_Creek', 'Terrey_Hills', 'Territory_Grape_Farm', 'Tewantin', 'Thargomindah', 'The_Monument', 'Thevenard_Island', 'Thredbo_Top_Station', 'Tibooburra_Airport', 'Tin_Can_Bay_Defence', 'Tindal', 'Tocal', 'Toowoomba', 'Townsville', 'Townsville_Air_Weapons_Range_Defence', 'Townsville__Fanning_River_Defence', 'Trangie', 'Trepell', 'Truscott', 'Tuggeranong', 'Tunnack', 'Ulladulla', 'Urandangi', 'Victoria_River_Downs', 'Viewbank', 'Wadeye_Port_Keats', 'Wagga_Wagga', 'Walgett', 'Walpeup', 'Walpole_North', 'Walungurru_Kintore', 'Wandering', 'Wangaratta', 'Warburto_Point', 'Warracknabeal_Airport', 'Warrnambool', 'Warwick', 'Wattamolla', 'Weipa', 'West_Wyalong', 'Westmere', 'White_Cliffs_AWS', 'Whyalla', 'Wilcannia_Airport', 'Williamtown', 'Willis_Island', 'Wilsons_Promontory', 'Wiluna_Airport', 'Windorah', 'Winton', 'Woolshed', 'Woomera', 'Wudinna_Airport', 'Wynyard', 'Yamba', 'Yampi_Sound_Defence', 'Yanco', 'Yarram_Airport', 'Yarrawonga', 'Yeppoon', 'Young', 'Yulara', 'Yunta', 'kunanyi__Mount_Wellington']`
                - `weather_variable`: weather variable to get data for, accepts values from `["TMAX","TMIN","PRCP","GUSTSPEED","GUSTDIR"]`
            - Optional URL Arguments:
                - `desired_units`: desired units to convert the output to, defaults to `None` (i.e. default dataset units)
                - `as_of`: an ISO formatted date representing the version of the data to use, defaults to `None` (i.e. current)
            - Example: `string request_URL = "/apiv3/australia-station-history/Brisbane/TMAX";`
        <!-- - `cme-history` -->
        <!-- - `cwv-station-history` -->
        <!-- - `dutch-station-history`
            - Inputs:  -->
        <!-- - `eaufrance` -->
        <!-- - `forecasts` -->
        <!-- - `german-station-history` -->
        <!-- - `german-station-hourly-history` -->
        <!-- - `ghcn-history` -->
        <!-- - `ghisd-station-history` -->
        <!-- - `grid-history`
            - Inputs:  -->
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
        - `string request_url`: the request URL following the format for API requests to `https://api.dclimate.net/` but excluding the root domain. See supported request types below
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
    - Request Type: `geo_temporal_query`
        - Request URL:
            - Format: `"/apiv4/geo_temporal_query/<dataset_name>?output_format=<desired_format>"`
            - URL Parameters:
                - `dataset_name`: name of geotemporal dataset, accepts values from `[agb-quarterly, chirps_final_05-daily, chirps_final_25-daily, chirps_prelim_05-daily, copernicus_ocean_salinity_0p5_meters-daily, copernicus_ocean_salinity_109_meters-daily, copernicus_ocean_salinity_1p5_meters-daily, copernicus_ocean_salinity_25_meters-daily, copernicus_ocean_salinity_2p6_meters-daily, copernicus_ocean_sea_level-daily, copernicus_ocean_temp_1p5_meters-daily, copernicus_ocean_temp_6p5_meters-daily, cpc_precip_global-daily, cpc_precip_us-daily, cpc_temp_max-daily, cpc_temp_min-daily, deforestation-quarterly, era5_2m_temp-hourly, era5_land_precip-hourly, era5_land_surface_pressure-hourly, era5_precip-hourly, era5_surface_solar_radiation_downwards-hourly, era5_wind_100m_u-hourly, era5_wind_100m_v-hourly, era5_wind_10m_u-hourly, era5_wind_10m_v-hourly, prism-precip-daily, prism-tmax-daily, prism-tmin-daily, vhi-weekly,]`
            - Optional URL Arguments:
                - `desired_format`: desired output format, accepts values from `[array]`, defaults to `array`
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
