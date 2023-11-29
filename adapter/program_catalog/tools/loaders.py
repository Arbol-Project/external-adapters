import os
import base64
import json
import ast
import typing
import inspect
import cloudpickle
from abc import abstractmethod
from functools import partial
from pydoc import locate
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

import program_catalog.tools.wrappers as client


def parse_timestamp(timestamp):
    ''' Helper funciton to parse timestamps to Pandas-readable date strings 

        Parameters: timestamp (number), a timestamp in seconds
        Returns: str, the date parsed to ISO format
    '''
    dt = datetime.fromtimestamp(timestamp)
    iso = dt.isoformat()
    return iso


def deserialize_config(config):
    if not isinstance(config, dict):
        return config
    deserialized_config = {}
    for k, v in config.items():
        if isinstance(v, dict):
            if '__class__' in v:
                value = load(v)
            else:
                value = deserialize_config(v)
        elif isinstance(v, list):
            value = [load(item)
                    if isinstance(item, dict) and all(x in item for x in ['__class__', '__config__'])
                    else deserialize_config(item)
                    for item in v]
        else:
            value = v
        deserialized_config[k] = value
    return deserialized_config


def load(doc: typing.Union[None, str, bytes, dict], parent_class: typing.Optional[typing.Type] = None):
    ''' Loads serialized class from a dictionary or a JSON string '''
    if doc is None:
        return None
    if isinstance(doc, (str, bytes)):
        doc = json.loads(doc)
    sub_class = locate(doc['__class__'])
    if parent_class is not None:
        if parent_class not in sub_class.mro():
            raise ValueError(f'Class {sub_class} must inherit from {parent_class}')
    return sub_class.from_dict(deserialize_config(doc.get('__config__', {})))


def cloud2obj(string):
    if not string.startswith(os.environ['OBJ_START']):
        raise ValueError('Unknown string')
    subs = string.split(os.environ['OBJ_START'])[-1]
    return cloudpickle.loads(base64.urlsafe_b64decode(subs.encode()))


def deserialize_func(serialized: typing.Union[None, str, dict]):
    '''
    Deserializes function
    '''
    if serialized is None:
        return None
    if isinstance(serialized, str):
        if serialized.startswith(os.environ['OBJ_START']):
            return cloud2obj(serialized)
        elif '.' in serialized:
            return locate(serialized)
    elif isinstance(serialized, dict):
        _serialized_func = serialized['func']
        if _serialized_func.startswith(os.environ['OBJ_START']):
            _func = partial(cloud2obj(_serialized_func), *serialized['args'], **serialized['kwargs'])
        else:
            _func = locate(_serialized_func)
            if _func is None:
                if not serialized['func'].startswith('risk.'):
                    raise ValueError('Functions outside "risk" cannot be deserialized')
                raise ValueError('Function path not found')
        return partial(_func, *serialized['args'], **serialized['kwargs'])
    return serialized


class SimplifiedSerializable:
    ''' This interface is a base for all contract data loaders
        used by the Arbol Chainlink External Adapter. At a high level it defines 
        (1) the sources/formats of data that the adapter accepts for building indexes,
        (2) the sources/formats of parametric inputs needed to evaluate the payout 
        of a contract using a constructed index, and 
        (3) the supported pairings of index data types and input schemes.

        1. Data Sources:
            - v3 dClimate grid data
            - v3 dClimate station data
            - v4 dClimate zarr grid data
            - dClimate IBTracs hurricane data (optionally downloaded from ncdc.noaa.gov @ https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r00/access/csv/)


        [actually this is not defined here but in the derivatives file]
        2. Parametric Inputs:
            - Serialized Risk Object (SRO): full JSON uploaded to IPFS (optionally unencrypted)
            - Simplified Contract Evaluator (SCE): small JSON stored on Polygon PoS (optionally unencrypted)
                - GRP/XSR:
                    v3 dClimate: 
                    {
                        "premium": number,
                        "limit": number,
                        "strike": float, 
                        "exhaust": number,
                        "tick": number,
                        "opt_type": string (PUT or CALL), 
                        "dataset": string,
                        "imperial_units": bool,
                        "locations": [float, float][]
                    }
                    v4 dClimate:
                    {
                        TODO
                    }
                - Blizzard Protection:
                    v3 dClimate:
                    {
                        TODO
                    }

        3. Supported Pairings:
            - Grid data ({v3 dClimate, v4 dClimate}, {SRO, SCE})
            - Station data ({v3 dClimate}, {SRO, SCE})
            - IBTracs data ({v3 dClimate, ncdc.noaa.gov}, {SRO})
    '''
    def __init__(self, **kwargs):
        if kwargs:
            print(f'Unused kwargs passed for {self.__class__.__name__}: {", ".join(["{}-{}".format(k, v) for k, v in kwargs.items()])}')

    @classmethod
    def from_dict(cls, doc):
        print('trying from_dict')
        skip = {'self', 'cls', 'args', 'kwargs'}
        parents = inspect.getmro(cls)[:-2]
        cls_args = set()
        for kls in parents:
            for method in ['__new__', '__init__']:
                for arg in inspect.signature(getattr(kls, method)).parameters.keys():
                    if arg not in skip and arg not in cls_args:
                        cls_args.add(arg)
        invalid_args = set(doc.keys()).difference(cls_args)
        if len(invalid_args) > 0 and 'kwargs' not in cls_args:
            for arg in invalid_args:
                doc.pop(arg)
        print('from_dict success')
        return cls(**doc)


class DataLoader(SimplifiedSerializable):
    ''' Base class for all data loaders. Defines the interface for all loaders
    '''
    def __init__(self, dataset_name=None, locations=None, post_process=None, **kwargs):
        self._dataset_name = dataset_name
        self._locations = locations
        self._post_process = deserialize_func(post_process)
        if self._post_process is not None and not callable(self._post_process):
            raise ValueError('"post_process" should be a callable, found: {}'.format(self._post_process))
        super().__init__(**kwargs)

    def load(self):
        result = self._load().sort_index()
        if result.index.duplicated().any():
            raise ValueError('Duplicates found in the index, please verify the data or the processing logic')
        if self._post_process is not None:
                result = self._post_process(result)
        if isinstance(result.index, pd.MultiIndex):
            pass
        elif not (isinstance(result.index, (pd.DatetimeIndex, pd.RangeIndex)) or result.index.is_numeric()):
            raise TypeError('Incorrect index type, should be of DatetimeIndex, Int64Index or RangeIndex with each '
                            'key as a year. Found: {}'.format(result.index))
        return result

    @abstractmethod
    def _load(self):
        raise NotImplementedError
    # getters
    def get_dataset_name(self):
        return self._dataset_name

    def get_location(self):
        return self._location

    def get_post_process_function(self):
        return self._post_process


class V3dClimateLoader(DataLoader):
    ''' Base loader class for dClimate weather data and Arbol dApp weather contracts. 
        Uses dWeather Python client to get historical weather data from IPFS and,
        in the case of contract evaluation requests computes a single time series 
        for a specified station or averaged over a number of locations
    '''
    def __init__(self, units_mult=1, data_name=None, imperial_units=False, desired_units=None, **kwargs):
        self._units_mult = units_mult if isinstance(units_mult, (int, float)) else deserialize_func(units_mult)
        # self._data_name = data_name
        self.units = getattr(self, 'units', None)
        self._request_params = getattr(self, '_request_params', {})
        
        if isinstance(imperial_units, str):
            imperial_units = ast.literal_eval(imperial_units)
        self._request_params.update({'use_imperial_units': imperial_units, 'desired_units': desired_units})
        super().__init__(**kwargs)

    def _load(self):
        series = self._ipfs_load()
        if self._data_name is not None:
            series = series.rename(self._data_name)
        return series * self._units_mult if isinstance(self._units_mult, (int, float)) else self._units_mult(series)
    # getters
    def _ipfs_load(self):
        raise NotImplementedError

    def get_units(self):
        return self.units

    def get_request_params(self):
        return self._request_params


class V4dClimateLoader(DataLoader):
    ''' Base loader class for dClimate weather data and Arbol dApp weather contracts
        that utilizes the v4 zarr multidimensional file format and storage architecture 
        deployed on IPFS.

        See dClimate API v4 for details
    '''
    def __init__(self, units_mult=1, data_name=None, as_of=None, point_limit=None, **kwargs):
        self._units_mult = units_mult if isinstance(units_mult, (int, float)) else deserialize_func(units_mult)
        self._data_name = data_name
        self.units = getattr(self, 'units', None)
        self._request_params = getattr(self, '_request_params', {})
        self._request_params.update({'as_of': as_of, 'point_limit': point_limit})
        super().__init__(**kwargs)

    def _load(self):
        series = self._ipfs_load()
        if self._data_name is not None:
            series = series.rename(self._data_name)
        return series * self._units_mult if isinstance(self._units_mult, (int, float)) else self._units_mult(series)
    # getters
    def _ipfs_load(self):
        raise NotImplementedError

    def get_units(self):
        return self.units

    def get_request_params(self):
        return self._request_params


class IBTracsLoader(DataLoader):
    ''' Loads hurricane data from NOAA 
    '''
    def __init__(self, region, freq='15min', start=1900, **kwargs):
        assert region in {'NA', 'EP', 'NI', 'SA', 'SI', 'SP', 'WP', 'ALL'}
        self._region = region
        print(f'Loading {region} hurricanes data...')
        self._freq = freq
        file_name = f'ibtracs.{region}.list.v04r00.csv'

        # only enable local read in development
        if os.path.exists(file_name):
            self._file = file_name
        else:
            self._file = 'https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs' \
                         '/v04r00/access/csv/' + self._file_name

        self._start = str(start)
        self._knots_to_mph = 1.15078
        super().__init__(**kwargs)

    def _load(self):
        full_df = pd.read_csv(self._file, low_memory=False)
        wind_columns = full_df.iloc[0]
        wind_columns = wind_columns[(wind_columns == 'kts') & (wind_columns.index.str.contains('WIND'))].index
        full_df.loc[:, 'BASIN'] = full_df.loc[:, 'BASIN'].fillna(self._region)
        fdf = full_df[full_df.BASIN == self._region]
        fdf = fdf.iloc[1:].replace(' ', np.nan)
        pdf = fdf.loc[:, ['SEASON', 'ISO_TIME', 'NUMBER', 'NAME', 'LAT', 'LON']]
        pdf['wind'] = fdf.loc[:, wind_columns].astype(float).max(axis=1) * self._knots_to_mph
        pdf.loc[:, ['LAT', 'LON']] = pdf.loc[:, ['LAT', 'LON']].astype(float)
        pdf.loc[:, ['SEASON', 'NUMBER']] = pdf.loc[:, ['SEASON', 'NUMBER']].astype(int)
        pdf = pdf.assign(
            dt=lambda dfx: pd.to_datetime(dfx.ISO_TIME)
        ).set_index('dt').drop(['ISO_TIME'], axis=1).dropna().sort_index().loc[self._start:]
        xpdf = pdf.groupby(
            ['SEASON', 'NUMBER', 'NAME']
        )[['LAT', 'LON', 'wind']].resample(self._freq).interpolate().sort_index()
        return xpdf.rename(columns={'LAT': 'lat', 'LON': 'lon'})


class GridcellLoader(V3dClimateLoader):
    ''' Loader class for grid file datasets. Uses dWeather Python client
        to get historical gridcell data from IPFS for specified locations and
        computes single time series averaged over all locations
    '''
    def __init__(self, locations, dataset_name: str, imperial_units=True, 
                as_of=None, **kwargs):
        ''' On initialization each Loader instance sets the locations for which to
            get the historical weather data and the dataset to pull from

            Parameters: locations (str), string of list of lat/lon coordinate pairs as strings
                        dataset_name (str), the name of the dataset on IPFS
                        imperial_units (bool), whether to use imperial units
                        kwargs (dict), additional request parameters
        '''
        kwargs['imperial_units'] = imperial_units
        if (type(locations) == str):
            kwargs['locations'] = ast.literal_eval(locations)
        else:
            kwargs['locations'] = locations
        if getattr(self, '_request_params', None) is None:
            self._request_params = {'dataset': dataset_name}
        if as_of:
            self._request_params['as_of'] = as_of
        super().__init__(**kwargs)

    def _ipfs_load(self):
        ''' Loads the weather data time series from IPFS for each specified
            location and averages the desired quantities to produce a single
            time series of historical averages

            Returns: Pandas Series, time series for desired weather data averaged
            across all locations specified during initialization
        '''
        gridcell_histories = []
        for (lat, lon) in self._locations:
            series = self._load_series(lat, lon)
            gridcell_histories.append(series)
        df = pd.concat(gridcell_histories, axis=1)
        result = pd.Series(df.mean(axis=1))
        return result

    def _load_series(self, lat, lon):
        ''' Loads a Pandas Series from IPFS for a given lat/lon coordinate pair

            Parameters: lat (float), latitude of location
                        lon (float), longitude of location
            Returns: Pandas Series, historical weather data for the given location
        '''
        data = client.get_gridcell_history_wrapper(lat, lon, **self._request_params)
        series = data['data']
        if series.empty:
            raise ValueError('No data returned for request')
        series = series.set_axis(pd.to_datetime(series.index, utc=True)).sort_index()
        return series


class StationLoader(V3dClimateLoader):
    ''' Loader class for GHCN station datasets. Uses dWeather Python client
        to get historical GHCN data from IPFS for specified weather station
    '''
    def __init__(self, dates: str, station_id: str, weather_variable: str, eval_start_date: str,
                dataset: str='ghcnd-imputed-daily', imperial_units=True, *args, **kwargs):
        ''' On initialization each Loader instance sets the locations for which to
            get the historical weather data and the dataset to pull from

            Parameters: dates (str), string of list of covered dates for contract as strings
                        station_id (str), id for weather station to get history from
                        weather_variable (str), the id for the weather condition to get history for 
                        dataset_name (str), name of dataset from which to get weather data
                        imperial_units (str), string of bool for whether to use imperial units
                        kwargs (dict), additional request parameters
        '''
        kwargs['imperial_units'] = imperial_units
        kwargs['locations'] = [station_id]
        if getattr(self, '_request_params', None) is None:
            self._request_params = {'dataset': dataset}
        self._request_params['weather_variable'] = weather_variable
        dates = ast.literal_eval(dates)
        self._dates = [date for date in dates if datetime.strptime(date, '%Y-%m-%d') < (eval_start_date + timedelta(days=15))]
        super().__init__(*args, **kwargs)

    def _ipfs_load(self):
        ''' Loads the dataset history from IPFS for the specified station ID
            and weather variable

            Returns: Pandas Series, time series for station weather data for covered dates
        '''
        data = client.get_station_history_wrapper(self._locations[0], **self._request_params)
        series = data['data']
        if series.empty:
            raise ValueError('No data returned for request')
        series = series.set_axis(pd.to_datetime(series.index)).sort_index()
        covered_dates = series.loc[self._dates]
        return covered_dates


class YieldLoader(V3dClimateLoader):
    ''' TODO '''
    def __init__(self, **kwargs):
        raise NotImplementedError


class GeoTemporalLoader(V4dClimateLoader):
    ''' Loader class for geotemporal datasets stored on IPFS in zarr format
    '''
    def __init__(self, dataset_name, 
                point_params,
                circle_params,
                rectangle_params,
                polygon_params,
                spatial_agg_params,
                temporal_agg_params,
                rolling_add_params,
                time_range,
                 **kwargs):
        pass
    # client.geo_temporal_query_wrapper()
