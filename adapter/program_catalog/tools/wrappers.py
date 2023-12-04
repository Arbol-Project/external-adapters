import os
import io
import json
import re
import ast
import pandas as pd
from datetime import timezone, datetime, date, time
from urllib.parse import urlparse

# from dweather_client import http_queries
from dweather_client import client as v3_client
from dclimate_zarr_client import client as v4_client

import time

PRECISION = 1e18

'''
UNSUPPORTED API ENDPOINTS:

ceda-biomass
cme-futures/stations
drought-monitor
irrigation_splits
metadata
rma-code-lookups/valid_counties
rma-code-lookups/valid_states
transitional_yield/valid_commodities
transitional_yield
user/get_token
yield/valid_commodities
yield
'''


# def convert_quantity(quant):
#     return None if quant is None else str(quant)


def get_australia_station_history_wrapper(args):
    ''' Returns dict with pd.Series "data" and string "unit"

        wrapped function returns:
            dict with datetime.date keys and weather variable Quantities (or strs in the case of GUSTDIR) as values
            string unit
    '''
    default_args = {"dataset": "bom_australia_stations-daily", "desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data, unit = v3_client.get_australia_station_history(**default_args)
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index)).sort_index()
    return {"data": data, "unit": unit}


# def get_ceda_biomass_wrapper(args):
#     ''' Returns dict with BytesIO "data" 
    
#         wrapped function returns:
#             BytesIO representing relevant GeoTiff File
#     '''
#     default_args = {"ipfs_timeout": None}
#     default_args.update(args)
#     data = v3_client.get_ceda_biomass(**args)
#     return data


def get_cme_station_futures_wrapper(args):
    ''' Returns dict with pd.Series "data" 
    
        wrapped function returns:
            dict with datetime.date keys and forecast data as values
    '''
    default_args = {"dataset": "cme_futures-daily", "desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    if default_args.get("forecast_date", None) is None:
        most_recent_metadata = v3_client.get_metadata(v3_client.get_heads()["cme_futures-daily"])
        forecast_date = datetime.datetime.strptime(most_recent_metadata["date range"][0], '%Y-%m-%d').date()
        default_args["forecast_date"] = forecast_date
    data = v3_client.get_station_forecast_history(**default_args)
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index)).sort_index()
    return {"data": data}

 
def get_cme_station_history_wrapper(args):
    ''' Returns dict with pd.Series "data" and string "unit" 

        wrapped function returns:
            dict with datetime.date keys and weather variable Quantities
            string unit
    '''
    default_args = {"desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data, unit = v3_client.get_cme_station_history(**default_args)
    # data = {k.__str__(): convert_quantity(v) for (k, v) in data.items()}
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index)).sort_index()
    return {"data": data, "unit": unit}


def get_cwv_station_history_wrapper(args):
    ''' Returns dict with pd.Series "data" 
    
        wrapped function returns:
            dict with datetime keys and cwv Quantities as values
    '''
    default_args = {"desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    # CWV is a proprietary unscaled unit from the UK National Grid
    data = v3_client.get_cwv_station_history(**default_args)
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index)).sort_index()
    return {"data": data}


# def get_drought_monitor_history_wrapper(args):
#     ''' Returns dict with pd.Series "data" 

#         wrapped function returns:
#             string containing drought monitor data in csv format
#     '''
#     default_args = {"ipfs_timeout": None}
#     default_args.update(args)
#     data = v3_client.get_drought_monitor_history(**args)
#     return {"data": data}
    

def get_dutch_station_history_wrapper(args):
    ''' Returns dict with pd.Series "data" and string "unit" 
    
        wrapped function returns:
            dict with datetime.date keys and weather variable Quantities as values
            string unit
    '''
    default_args = {"dataset": "dutch_stations-daily", "desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data, unit = v3_client.get_european_station_history(**default_args)
    # data = {k.__str__(): convert_quantity(v) for (k, v) in data.items()}
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index)).sort_index()
    return {"data": data, "unit": unit}


def get_eaufrance_history_wrapper(args):
    ''' Returns dict with pd.Series "data" and string "unit" 
    
        wrapped function returns:
            dict with datetime.date keys and flowrates as values
            string unit
    '''
    default_args = {"desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data, unit = v3_client.get_eaufrance_history(**default_args)
    # data = {k.__str__(): convert_quantity(v) for (k, v) in data.items()}
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index)).sort_index()
    return {"data": data, "unit": unit}


def get_forecasts_wrapper(args):
    ''' Returns dict with pd.Series "data" and string "unit" 
    
        wrapped function returns:
            dict with pd.Series keys and and values
            string unit
    '''
    default_args = {"also_return_metadata": False, "also_return_snapped_coordinates": True, "use_imperial_units": True, "desired_units": None, "ipfs_timeout": None, "convert_to_local_time": True}
    default_args.update(args)
    data, unit = v3_client.get_forecast(**default_args)
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    # data = data.set_axis(pd.to_datetime(data.index, utc=True)).sort_index()
    return {"data": data, "unit": unit}


def get_german_station_history_wrapper(args):
    ''' Returns dict with pd.Series "data" and string "unit" 
    
        wrapped function returns:
            dict with datetime.date keys and weather variable Quantities as values
            string unit
    '''
    default_args = {"dataset": "dwd_stations-daily", "desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data, unit = v3_client.get_european_station_history(**default_args)
    # data = {k.__str__(): convert_quantity(v) for (k, v) in data.items()}
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index)).sort_index()
    return {"data": data, "unit": unit}


def get_german_hourly_station_history_wrapper(args):
    ''' Returns dict with pd.Series "data" and string "unit" 
    
        wrapped function returns:
            dict with datetime keys and weather variable Quantities as values
            string unit
    '''
    default_args = {"dataset": "dwd_hourly-hourly", "desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data, unit = v3_client.get_hourly_station_history(**default_args)
    # data = {k.__str__(): convert_quantity(v) for (k, v) in data.items()}
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index)).sort_index()
    return {"data": data, "unit": unit}


def get_station_history_wrapper(args):
    ''' Returns dict with pd.Series "data" and string "unit" 
    
        wrapped function returns:
            dict with datetime.date keys and weather variable Quantities as values
            string unit
    '''
    default_args = {"desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data, unit = v3_client.get_station_history(**default_args)
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index)).sort_index()
    return {"data": data, "unit": unit}


def get_ghisd_station_history_wrapper(args):
    ''' Returns dict with pd.Series "data" and string "unit" 
    
        wrapped function returns:
            dict with datetime.date keys and weather variable Quantities as values
            string unit
    '''
    default_args = {"dataset": "ghisd-sub_hourly", "use_imperial_units": True, "desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data, unit = v3_client.get_hourly_station_history(**default_args)
    # data = {k.__str__(): convert_quantity(v) for (k, v) in data.items()}
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index)).sort_index()
    return {"data": data, "unit": unit}


def get_gridcell_history_wrapper(args):
    ''' Returns dict with pd.Series "data" and string "unit"
     
        wrapped function returns:
            dict with datetime/datetime.date keys and climate values
            string unit  
    '''
    default_args = {"also_return_metadata": False, "also_return_snapped_coordinates": False, "use_imperial_units": True, "desired_units": None, "ipfs_timeout": None, "as_of": None, "convert_to_local_time": True}
    default_args.update(args)
    data, unit = v3_client.get_gridcell_history(**default_args)
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index, utc=True)).sort_index()
    return {"data": data, "unit": unit}


def get_inmet_station_history_wrapper(args):
    ''' Returns dict with pd.Series "data" and string "unit" 
    
        wrapped function returns:
            dict with datetime.date keys and weather variable Quantities as values
            string unit
    '''
    default_args = {"dataset": "inmet_brazil-hourly", "desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data, unit = v3_client.get_csv_station_history(**default_args)
    # data = {k.__str__(): convert_quantity(v) for (k, v) in data.items()}
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index)).sort_index()
    return {"data": data, "unit": unit}


# def get_irrigation_data_wrapper(args):
#     ''' Returns dict with pd.DataFrame data 
    
#         wrapped function returns:
#             string containing irrigation data for commodity in csv format
#     '''
#     default_args = {"ipfs_timeout": None}
#     default_args.update(args)
#     data = v3_client.get_irrigation_data(**default_args)
#     return data


def get_japan_station_history_wrapper(args):
    ''' Returns dict with pd.Series "data" and string "unit" 
    
        wrapped function returns:
            dict with datetime keys and temperature Quantities as values\
            string unit
    '''
    default_args = {"ipfs_timeout": None}
    default_args.update(args)
    data, unit = v3_client.get_japan_station_history(**default_args)
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index)).sort_index()
    return {"data": data, "unit": unit}


# def get_metadata_wrapper(args):
#     ''' Returns dict '''
#     head_hash = v3_client.get_heads()[args['dataset']]
#     metadata = v3_client.get_metadata(head_hash)
#     if args.get('full_metadata', False):
#         return metadata
#     if args['dataset'] in v3_client.GRIDDED_DATASETS.keys():
#         return {
#             **metadata["api documentation"],
#             "name": metadata["name"],
#             "update frequency": metadata["update frequency"],
#             "time last generated": metadata["time generated"],
#             "latitude range": metadata["latitude range"],
#             "longitude range": metadata["longitude range"],
#         }
#     elif args['dataset'] in ["ghcnd", "ghcnd-imputed-daily"]:
#         return {
#             **metadata["api documentation"],
#             "name": metadata["name"],
#             "update frequency": metadata["update frequency"],
#             "stations url": http_queries.GATEWAY_URL + f"/ipfs/{head_hash}/{metadata['stations file']}",
#             "time last generated": metadata["time generated"]
#         }
#     return metadata


def get_power_history_wrapper(args):
    ''' Returns dict with pd.Series "data" and string "unit" 
    
        wrapped function returns:
            dict with datetime.date keys and weather variable Quantities as values
            string unit
    '''
    default_args = {"dataset": "ne_iso-hourly", "station_id": "NEW_ENGLAND", "weather_variable": "RTDMND", "desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data, unit = v3_client.get_csv_station_history(**default_args)
    # data = {k.__str__(): convert_quantity(v) for (k, v) in data.items()}
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index)).sort_index()
    return {"data": data, "unit": unit}


def get_tropical_storms_wrapper(args):
    ''' Returns dict with pd.DataFrame "data"
    
        wrapped function returns:
            pd.DataFrame containing time series information on tropical storms
    '''
    default_args = {"ipfs_timeout": None}
    default_args.update(args)
    data = v3_client.get_tropical_storms(**args)
    return {"data": data}


def get_teleconnections_history_wrapper(args):
    ''' Returns dict with pd.Series "data"
    
        wrapped function returns:
            dict with datetime.date keys and teleconnection index Quantities as values
    '''
    default_args = {"desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data = v3_client.get_teleconnections_history(**default_args)
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index)).sort_index()
    return {"data": data}


# def get_transitional_yield_history_wrapper(args):
#     ''' Returns dict with pd.DataFrame "data" 
    
#         wrapped function returns:
#             string containing yield data in csv format
#     '''
#     if args.get('impute', False):
#         args['dataset'] = 'rma_t_yield_imputed-single-value'
#     else:
#         args['dataset'] = 'rma_t_yield-single-value'
#     default_args = {"impute": False}
#     default_args.update(args)
#     data = v3_client.get_yield_history(**default_args)
#     return data


def get_sap_station_history_wrapper(args):
    ''' Returns dict with pd.Series "data"
    
        wrapped function returns:
            dict with datetime keys and sap Quantities as values
    '''
    default_args = {"desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data = v3_client.get_sap_station_history(**default_args)
    data = pd.Series(data)
    if data.empty:
        raise ValueError('No data returned for request')
    data = data.set_axis(pd.to_datetime(data.index)).sort_index()
    return {"data": data}


# def get_yield_history_wrapper(args):
#     ''' Returns dict with pd.DataFrame "data" 
    
#         wrapped function returns:
#             string containing yield data in csv format
#     '''
#     if args.get('impute', False):
#         args['dataset'] = 'rmasco_imputed-yearly'
#     elif args.get('fill', False):
#         args['dataset'] = 'sco_vhi_imputed-yearly'
#     else:
#         args['dataset'] = 'sco-yearly'
#     default_args = {"impute": False, "fill": False}
#     default_args.update(args)
#     data = v3_client.get_yield_history(**default_args)
#     return data


def geo_temporal_query_wrapper(args):
    ''' Returns dict with pd.Series 
    
        wrapped function returns:
            numpy array of data values
    '''
    default_args = {"as_of": None, "point_limit": None}
    default_args.update(args)
    start = time.time()
    try:
        result = v4_client.geo_temporal_query(**default_args)
        print(f'geo_temporal_query took {time.time() - start} seconds')
        if type(result) is dict:
            result["data"] = int(float(result["data"][0]) * PRECISION)
            result["unit"] = f'{result.get("unit of measurement", None)} * {PRECISION}'
        return result
    except Exception as e:
        print(f'error caught in geo_temporal_query_wrapper: {e}')
        raise ValueError('Request errored')


def get_api_mapping(swagger_dir):
    supported_client_wrappers = {
        'australia-station-history': get_australia_station_history_wrapper,
        # 'ceda-biomass': get_ceda_biomass_wrapper,
        # 'cme-futures/stations': get_cme_futures_stations_wrapper,
        'cme-futures': get_cme_station_futures_wrapper,
        'cme-history': get_cme_station_history_wrapper,
        'cwv-station-history': get_cwv_station_history_wrapper,
        # 'drought-monitor': get_drought_monitor_history_wrapper,
        'dutch-station-history': get_dutch_station_history_wrapper,
        'eaufrance': get_eaufrance_history_wrapper,
        'forecasts': get_forecasts_wrapper,
        'german-station-history': get_german_station_history_wrapper,
        'german-station-hourly-history': get_german_hourly_station_history_wrapper,
        'ghcn-history': get_station_history_wrapper,
        'ghisd-station-history': get_ghisd_station_history_wrapper,
        'grid-history': get_gridcell_history_wrapper,
        'inmet': get_inmet_station_history_wrapper,
        # 'irrigation_splits': get_irrigation_data_wrapper,
        'japan-station-history': get_japan_station_history_wrapper,
        # 'metadata': get_metadata_wrapper,
        'power-history/ne_iso/load': get_power_history_wrapper,
        # 'rma-code-lookups/valid_counties': get_rma_code_lookups_counties_wrapper,
        # 'rma-code-lookups/valid_states': get_rma_code_lookups_states_wrapper,
        'storms': get_tropical_storms_wrapper,
        'teleconnections': get_teleconnections_history_wrapper,
        # 'transitional_yield/valid_commodities': get_transitional_yield_commodities_wrapper,
        # 'transitional_yield': get_transitional_yield_history_wrapper,
        'uk-national-grid/sap': get_sap_station_history_wrapper,
        # 'yield/valid_commodities': get_yield_commodities_wrapper,
        # 'yield': get_yield_history_wrapper,
        'geo_temporal_query': geo_temporal_query_wrapper,
    }
    api_versions = {}
    for file in os.listdir(swagger_dir):
        file_path = os.path.join(swagger_dir, file)
        with open(file_path, 'r') as swagger:
            api = json.load(swagger)
            swagger.close()
        # parse swagger and get parameters and url endpoints
        api_map = {'basePath': api['basePath'] + '/', 'paths': {}}
        for path in api['paths'].keys():
            if 'user' in path or 'valid' in path or 'biomass' in path:
                continue
            key = path[:path.find('/{')][1:] if '/{' in path else path[1:]
            if not key in supported_client_wrappers:
                continue
            types = {}
            primary = re.findall(r'(?<=\{).+?(?=\})', path) if '/{' in path else []
            secondary = []
            for param in api['paths'][path].get('parameters', []):
                types[param['name']] = param['type']
            for param in api['paths'][path].get('get', {}).get('parameters', []):
                if param['name'] != 'Authorization':
                    secondary.append(param['name'])
                    types[param['name']] = param['type']
            api_map['paths'][key] = {'name': path, 'primary': primary, 'secondary': secondary, 'types': types, 'function': supported_client_wrappers[key]}
        api_versions[api['basePath']] = api_map
    
    return api_versions


def parse_v3_request(data, req, map):
    # get endpoint
    request_parsed = list(urlparse(data))
    print(f'request_parsed: {request_parsed}')
    request_paths = request_parsed[2].split('/')
    print(f'request_paths: {request_paths}')
    key = request_paths[1]
    if key == 'drought-monitor':
        print('replacing "-" separator with "_" in drought-monitor parameters')
        request_paths[1] = request_paths[1].replace('-', '_')
        print(f'new request_paths: {request_paths}')
    api_endpoint = map['paths'].get(key, None)
    if api_endpoint is None:
        print(f'api_endpoint not found for key {key} and map {list(map["paths"].keys())}')
        return 'Improperly formatted request URL, endpoint not found', False, None, []

    # get primary parameters
    args = {}
    endpoint_primaries = api_endpoint['primary']
    endpoint_secondaries = api_endpoint['secondary']
    if 'dataset' in endpoint_primaries:
        params = [request_paths[1]]
        for req in request_paths[2:]:
            params += req.split('_')
    else:
        params = re.split('_|/', request_parsed[2])[2:]
    if request_parsed[4] == '':
        queries = []
    else:
        queries = request_parsed[4].split('&')
    if len(params) != len(endpoint_primaries):
        print(f'params: {params}, endpoint_primaries: {endpoint_primaries}')
        return 'Improperly formatted request URL, incompatible parameters', False, None, []

    # cast floats and set primary args
    floats = ['lat', 'lon', 'radius', 'max_lat', 'max_lon', 'min_lat', 'min_lon']
    for i in range(len(endpoint_primaries)):
        param = endpoint_primaries[i]
        if param in floats:
            args[param] = float(params[i])
        else:
            args[param] = params[i]

    # parse secondary parameters
    for j in range(len(queries)):
        param = queries[j][:queries[j].find('=')]
        value = queries[j][queries[j].find('='):][1:]
        param_type = map['paths'][key]['types'][param]
        if not param in endpoint_secondaries:
            return 'Improperly formatted request URL, incompatible parameters', False, None, []

        # type check parameters and set secondary args
        if param in floats:
            args[param] = float(params[i])
        if param_type != 'string':
            if param_type == 'boolean':
                value = value.capitalize()
            value = ast.literal_eval(value)
        args[param] = value
    args['_key'] = key
    return args, True, req.get('request_ops', None), req.get('request_params', [])


def parse_v4_request(data, req, map):
    geo_temporal_parameters = {
        'point_params': (["lat", "lon"], [float, float]),
        'circle_params': (["center_lat", "center_lon", "radius"], [float, float, float]),
        'rectangle_params': (["min_lat", "min_lon", "max_lat", "max_lon"], [float, float, float, float]),
        'polygon_params': (["epsg_crs"], [int]),
        'multiple_points_params': (["epsg_crs"], [int]),
        'spatial_agg_params': (["agg_method"], [str]),
        'time_range': ([], [datetime.fromisoformat, datetime.fromisoformat]),
        'temporal_agg_params': (["time_period", "agg_method", "time_unit"], [str, str, int]),
        'rolling_add_params': (["window_size", "agg_method"], [int, str]),
    }
    request_data = list(urlparse(data))
    print(f'request_data: {request_data}')
    request_paths = request_data[2].split('/')
    print(f'request_paths: {request_paths}')
    key = request_paths[1]
    dataset_name = request_paths[2]
    if request_data[4] != '':
        output_format = request_data[4].split('=')[1]
    else:
        output_format = 'array'
    args = {
        '_key': key,
        'dataset_name': dataset_name,
        'output_format': output_format
    }
    spatial_parameters = req.get('spatial_parameters', [])
    temporal_parameters = req.get('temporal_parameters', [])
    parameters = spatial_parameters + temporal_parameters
    length = len(parameters)
    idx = 0
    while idx < length:
        possible_label = parameters[idx]
        if possible_label in geo_temporal_parameters:
            labels, transforms = geo_temporal_parameters[possible_label]
            if len(labels) == 0:
                param_list = []
                for i, transform in enumerate(transforms):
                    param_list.append(transform(parameters[idx+i+1]))
                relabel = possible_label.replace('_params', '_kwargs')
                args[relabel] = param_list
            else:
                param_dict = {}
                for i, label in enumerate(labels):
                    param_dict[label] = transforms[i](parameters[idx+i+1])
                relabel = possible_label.replace('_params', '_kwargs')
                args[relabel] = param_dict
            idx += len(transforms)
        else:
            idx += 1
    return args, True, None, []


API_MAPS = get_api_mapping('./swaggers')


def parse_request(data, req):
    parsers = {
        "/apiv3": parse_v3_request,
        "/apiv4": parse_v4_request,
    }
    # check basePath version
    for base_path in API_MAPS.keys():
        if data.startswith(base_path):
            return parsers[base_path](data.removeprefix(base_path), req, API_MAPS[base_path])


def get_request_data(args):
    key = args.pop('_key')
    for base_path in API_MAPS.keys():
        if key in API_MAPS[base_path]['paths'].keys():
            api_endpoint = API_MAPS[base_path]['paths'][key]
            data = api_endpoint['function'](args)
            if "unit" not in data:
                data["unit"] = None
            return data
    raise ValueError('Request not supported')


def operate_on_data(data, ops, args):
    ''' 
        data is dict iff metadata and BytesIO iff CEDA (basically not supported)
            and pd.Series/pd.DataFrame otherwise 
        18 digits of precision on decimals 
        times are returned as timestamps starting at beginning of unix epoch
        dates are returned as timestamps starting at beginning of unix epoch to start of date
        ms on timestamps
    '''
    if type(data) is dict or type(data) is io.BytesIO:
        return 0, "Request not supported"
    reset = data
    for i, op in enumerate(ops):
        pandas_op = getattr(data, op)
        op_params = ast.literal_eval(args[i])
        return_result = op_params.pop(0)
        carry_forward = op_params.pop(0)
        result = pandas_op(*op_params)
        if return_result:
            if type(result) is pd.Series or type(result) is pd.DataFrame:
                result = result.mean()
            if type(result) is date:
                result = datetime(result.year, result.month, result.day)
            if type(result) is time:
                result = datetime(0, 0, 0, result.hour, result.minute, result.second, result.microsecond)
            if type(result) is datetime:
                return int(result.replace(tzinfo=timezone.utc).timestamp() * 1000), "ms since epoch", None
            elif 'float' in str(type(result)) or 'int' in str(type(result)):
                if not data["unit"]:
                    return int(float(result) * PRECISION), data["unit"], None
                else:
                    return int(float(result) * PRECISION), f'{data["unit"]} * {PRECISION}', None
            else:
                return 0, "Incompatible return type"
        if carry_forward:
            data = result
        else:
            data = reset
    return 0, "No return specified"