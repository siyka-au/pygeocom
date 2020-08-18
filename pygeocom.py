from typing import Tuple, Any
from inspect import signature

class geocom_command:
    def __init__(self, rpc_id: int):
        self.rpc_id = rpc_id

    def __call__(self, f):
        rpc_id = self.rpc_id
        def wrapped_f(self) -> Tuple[Any, ...]:
            self.stream.write('\n%R1Q,{}:\r\n'.format(rpc_id).encode('ascii'))
            header, parameters = self.stream.readline().split(':', 1)
            reply_type, return_code, transaction_id = header.split(b',')
            return_code = int(return_code)
            transaction_id = int(transaction_id)
            return reply
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

    @geocom_command(5035
    def get_device_config(self) -> (int, int):
        pass
