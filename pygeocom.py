

class PyGeoCom:
    def __init__(self, stream):
        # Do nothing
        self.stream = stream
        self.stream.write(b'\n')

    def get_instrument_number(self) -> str:
        r = self.request(5003)
        None

    def request(self, code: int) -> str:
        self.stream.write('\n%R1Q,{}:\r\n'.format(code).encode('ascii'))
        r = self.stream.readline()
        return r
