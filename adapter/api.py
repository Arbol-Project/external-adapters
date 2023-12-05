from program_catalog.tools.wrappers import parse_request, get_request_data, operate_on_data


class dClimateAdapter:
    ''' External Adapter class for retrieving dClimate weather data on IPFS,
        performing chained operations, and returning the result on chain 
    '''

    def __init__(self, data):
        ''' Each call to the adapter creates a new Adapter
            instance to handle the request

            Parameters: input (dict), the received request body
        '''
        self.id = data.get('id', '2')
        self.request_data = data.get('data')
        self.validate_request_data()
        if self.valid:
            self.execute_request()
        else:
            self.result_error()

    def validate_request_data(self):
        ''' Validate that the received request is properly formatted and includes
            all necessary paramters. In the case of an illegal request error
            information is logged to the output
        '''
        if self.request_data is None or self.request_data == {}:
            self.request_error = 'request data empty'
            self.valid = False
        else:
            request_url = self.request_data.get('request_url', None)
            if request_url is None:
                self.request_error = 'request_url missing'
                self.valid =  False
            else:
                try:
                    result, valid, request_ops, request_params = parse_request(request_url, self.request_data)
                    if not valid:
                        self.request_error = result
                        self.valid = False
                    else:
                        self.request_args = result
                        self.request_operations = request_ops # self.request_data.get('request_ops', None)
                        self.request_parameters = request_params # self.request_data.get('request_params', [])
                        self.valid = True
                except Exception as e:
                    self.valid = False
                    self.request_error = e

    def execute_request(self):
        ''' Get the designated program and determine whether the associated
            contract should payout and if so then for how much
        '''
        try:
            result = get_request_data(self.request_args)
            if self.request_operations is not None:
                result['data'], result["unit"], msg = operate_on_data(result['data'], self.request_operations, self.request_parameters)
                if msg is not None:
                    self.request_error = msg
                    self.result_error()
                else:
                    payload = {'unit': result['unit'], 'data': result['data']}
                    self.result_success(payload)
            else:
                # currently only supporting return values and units, not metadata, snapped cooordinates, etc
                # also first just one return value at a time (along with unit)
                # unit is now a failure message if fail, adapter no longer returns 500 response on fail
                payload = {'unit': result['unit'], 'data': result['data']}
                self.result_success(payload)
        except Exception as e:
            print(e)
            raise e
            # self.request_error = e
            # self.result_error()

    def result_success(self, result):
        ''' If the request reaches no errors log the outcome in the result field
            including the payout in the response

            Parameters: result (float), the determined payout value
        '''
        self.result = {
            'jobRunID': self.id,
            'result': result,
            'statusCode': 200,
        }

    def result_error(self):
        ''' If the request terminates in an error then log the error details in
            the result field to be returned in the response

            Parameters: error (str), associated error message
        '''
        print(f'error message: {self.request_error}')
        self.result = {
            'jobRunID': self.id,
            'result': {'unit': self.request_error, 'data': 0},
            'statusCode': 200,
        }


'''
curl -X POST "http://127.0.0.1:8000/api" \
-H "content-type:application/json" \
--data-binary @- << EOF
{
    "id": 0,
    "data": {
        "request_url": "/apiv3/grid-history/era5_land_precip-hourly/1.375_103.875?also_return_metadata=false&use_imperial_units=true&also_return_snapped_coordinates=false&convert_to_local_time=true",
        "request_ops": ["last", "mean"],
        "request_params": ["[False, True, '1M']", "[True, False]"]
        }
}
EOF

curl -X POST "http://127.0.0.1:8000/api" \
-H "content-type:application/json" \
--data-binary @- << EOF
{
    "id": 0,
    "data": {
        "request_url": "/apiv3/dutch-station-history/210/WINDSPEED?use_imperial_units=true",
        "request_ops": ["last", "max"],
        "request_params": ["[False, True, '1M']", "[True, False]"]
        }
}
EOF

curl -X POST "http://127.0.0.1:8000/api" \
-H "content-type:application/json" \
--data-binary @- << EOF
{
    "id": 0,
    "data": {
        "request_url": "/apiv4/geo_temporal_query/cpc_temp_min-daily?output_format=array",
        "spatial_parameters": ["point_params", "1.375", "103.875"],
        "temporal_parameters": ["time_range", "2022-09-01", "2022-09-30", "temporal_agg_params", "all", "max", "1"]
        }
}
EOF

curl -X POST "http://127.0.0.1:8000/api" \
-H "content-type:application/json" \
--data-binary @- << EOF
{
    "id": 0,
    "data": {
        "request_url": "/apiv4/geo_temporal_query/chirps_final_25-daily?output_format=array",
        "spatial_parameters": ["point_params", "1.375", "103.875"],
        "temporal_parameters": ["time_range", "2022-09-01", "2022-09-30", "temporal_agg_params", "all", "max", "1"]
        }
}
EOF
'''