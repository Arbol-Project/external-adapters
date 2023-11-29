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
n.b. - making change to schema at drought_monitoring ({state}-{county} changed to {state}_{county} as elsewhere),
     the importance being that it is now assumed that '-' is not a separating character for parameters in a request URL

not implemented

ceda-biomass
rma-code-lookups/valid_counties
rma-code-lookups/valid_states
transitional_yield/valid_commodities
yield/valid_commodities
get_csv_station_history
get_hourly_station_history
'''

# def get_ceda_biomass_wrapper(args):
#     ''' Returns dict with BytesIO data '''
#     data = v3_client.get_ceda_biomass(**args)
#     return data


def get_forecasts_wrapper(args):
    ''' Returns dict with pd.Series data and units '''
    default_args = {"also_return_metadata": False, "also_return_snapped_coordinates": True, "use_imperial_units": True, "desired_units": None, "ipfs_timeout": None, "convert_to_local_time": True}
    default_args.update(args)
    data = v3_client.get_forecast(**default_args)
    return data


# def get_drought_monitor_history_wrapper(args):
#     ''' Returns dict with pd.Series data '''
#     data = v3_client.get_drought_monitor_history(**args)
#     return data

 
def get_cme_station_history_wrapper(args):
    ''' Returns dict with pd.Series data and units '''
    default_args = {"desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data = v3_client.get_cme_station_history(**default_args)
    return data


def get_dutch_station_history_wrapper(args):
    ''' Returns dict with pd.Series data and units '''
    default_args = {"dataset": "dutch_stations-daily", "desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data = v3_client.get_european_station_history(**default_args)
    data['data'] = pd.Series(data['data'])
    if data.empty:
        raise ValueError('No data returned for request')
    data['data'] = data['data'].set_axis(pd.to_datetime(data['data'].index)).sort_index()
    return data


def get_german_station_history_wrapper(args):
    ''' Returns dict with pd.Series data and units '''
    default_args = {"dataset": "dwd_stations-daily", "desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data = v3_client.get_european_station_history(**default_args)
    data['data'] = pd.Series(data['data'])
    if data.empty:
        raise ValueError('No data returned for request')
    data['data'] = data['data'].set_axis(pd.to_datetime(data['data'].index)).sort_index()
    return data


def get_japan_station_history_wrapper(args):
    ''' Returns dict with pd.Series data and units '''
    default_args = {"ipfs_timeout": None}
    default_args.update(args)
    data = v3_client.get_japan_station_history(**default_args)
    return data


# def get_tropical_storms_wrapper(args):
#     ''' Returns dict with pd.DataFrame data '''
#     data = v3_client.get_tropical_storms(**args)
#     return data


# def get_irrigation_data_wrapper(args):
#     ''' Returns dict with pd.DataFrame data '''
#     default_args = {"ipfs_timeout": None}
#     default_args.update(args)
#     data = v3_client.get_irrigation_data(**default_args)
#     return data


# def get_transitional_yield_history_wrapper(args):
#     ''' Returns dict with pd.DataFrame data '''
#     if args.get('impute', False):
#         args['dataset'] = 'rma_t_yield_imputed-single-value'
#     else:
#         args['dataset'] = 'rma_t_yield-single-value'
#     default_args = {"impute": False}
#     default_args.update(args)
#     data = v3_client.get_yield_history(**default_args)
#     return data


# def get_yield_history_wrapper(args):
#     ''' Returns dict with pd.DataFrame data '''
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


def get_station_history_wrapper(args):
    ''' Returns dict with pd.Series data and units '''
    default_args = {"dataset": "ghcnd", "station_id": "USW00003016", "use_imperial_units": True, "desired_units": None, "ipfs_timeout": None}
    default_args.update(args)
    data = v3_client.get_station_history(**default_args)
    data['data'] = pd.Series(data['data'])
    if data.empty:
        raise ValueError('No data returned for request')
    data['data'] = data['data'].set_axis(pd.to_datetime(data['data'].index)).sort_index()
    return data


def get_gridcell_history_wrapper(args):
    ''' Returns dict with pd.Series data and units '''
    default_args = {"also_return_metadata": False, "also_return_snapped_coordinates": True, "use_imperial_units": True, "desired_units": None, "ipfs_timeout": None, "as_of": None, "convert_to_local_time": True}
    default_args.update(args)
    data = v3_client.get_gridcell_history(**default_args)
    data['data'] = data['data'].set_axis(pd.to_datetime(data['data'].index, utc=True)).sort_index()
    return data


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


def get_api_mapping(file_path):
    client_wrapper = {
        # 'geo_temporal_query': geo_temporal_query_wrapper,
        # 'ceda-biomass': get_ceda_biomass_wrapper,
        'cme-history': get_cme_station_history_wrapper,
        # 'drought-monitor': get_drought_monitor_history_wrapper,
        'dutch-station-history': get_dutch_station_history_wrapper,
        'forecasts': get_forecasts_wrapper,
        'german-station-history': get_german_station_history_wrapper,
        'ghcn-history': get_station_history_wrapper,
        'grid-history': get_gridcell_history_wrapper,
        # 'irrigation_splits': get_irrigation_data_wrapper,
        # 'metadata': get_metadata_wrapper,
        # 'storms': get_tropical_storms_wrapper,
        # 'transitional_yield': get_transitional_yield_history_wrapper,
        # 'yield': get_yield_history_wrapper,
        'japan-station-history': get_japan_station_history_wrapper
    }
    with open(file_path, 'r') as swagger:
        api = json.load(swagger)
        swagger.close()

    # parse swagger and get parameters and url endpoints
    api_map = {'basePath': api['basePath'] + '/', 'paths': {}}
    for path in api['paths'].keys():
        if 'user' in path or 'valid' in path or 'biomass' in path:
            continue
        key = path[:path.find('/{')][1:] if '/{' in path else path[1:]
        if not key in client_wrapper:
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
        api_map['paths'][key] = {'name': path, 'primary': primary, 'secondary': secondary, 'types': types, 'function': client_wrapper[key]}
    return api_map

API_MAP = get_api_mapping('swagger.json')


#  section for zarr based geotemporal queries
def geo_temporal_query_wrapper(args):
    ''' Returns dict with pd.Series '''
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


def parse_zarr_request(data, req):
    request_data = list(urlparse(data))
    request_paths = request_data[2].split('/')
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


def parse_request(data, req):
    # check basePath version
    v3_base_path = API_MAP['basePath']
    if not data.startswith(v3_base_path):
        v4_base_path = "/apiv4"
        if data.startswith(v4_base_path):
            return parse_zarr_request(data.removeprefix(v4_base_path), req)
        else:
            return f'Incompatible API version, please use {v3_base_path} or {v4_base_path}', False, None, []
        
    request_data = data.removeprefix(v3_base_path)

    # get endpoint
    request_parsed = list(urlparse(request_data))
    request_paths = request_parsed[2].split('/')
    key = request_paths[0]
    api_endpoint = API_MAP['paths'].get(key, None)
    if api_endpoint is None:
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
        params = re.split('_|/', request_parsed[2])[1:]
    if request_parsed[4] == '':
        queries = []
    else:
        queries = request_parsed[4].split('&')
    if len(params) != len(endpoint_primaries):
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
        param_type = API_MAP['paths'][key]['types'][param]
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


def get_request_data(args):
    key = args.pop('_key')
    if key == "geo_temporal_query":
        return geo_temporal_query_wrapper(args)
    api_endpoint = API_MAP['paths'].get(key, None)
    data = api_endpoint['function'](args)
    if "unit" not in data:
        data["unit"] = None
    return data


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