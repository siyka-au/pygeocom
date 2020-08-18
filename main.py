import serial
from pygeocom import PyGeoCom

def main():
    ser = serial.Serial('/dev/ttyUSB0', 19200, timeout=1)
    
    geo = PyGeoCom(ser)

    print(geo.get_instrument_number())
    print(geo.get_instrument_name())
    print(geo.get_device_config())

    ser.close()

if __name__ == "__main__":
    main()
