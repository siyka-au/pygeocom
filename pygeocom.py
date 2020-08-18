from typing import Tuple, Any
from inspect import signature

class geocom_command:
    def __init__(self, rpc_id: int):
        self.rpc_id = rpc_id

    def __call__(self, f):
        rpc_id = self.rpc_id
        def wrapped_f(self) -> Tuple[Any, ...]:
            self.stream.write('\n%R1Q,{}:\r\n'.format(rpc_id).encode('ascii'))
            header, parameters = self.stream.readline().split(b':', 1)
            
            reply_type, geocom_return_code, transaction_id = header.split(b',')
            geocom_return_code = int(geocom_return_code)
            transaction_id = int(transaction_id)

            parameters = parameters.rstrip()
            rpc_return_code, *parameters = parameters.split(b',')
            rpc_return_code = int(rpc_return_code)
            
            return parameters
        return wrapped_f

class PyGeoCom:
    def __init__(self, stream):
        # Do nothing
        self.stream = stream
        self.stream.write(b'\n')

    @geocom_command(5003)
    def get_instrument_number(self) -> int:
        pass

    @geocom_command(5004)
    def get_instrument_name(self) -> str:
        pass

    @geocom_command(5035)
    def get_device_config(self) -> (int, int):
        pass
