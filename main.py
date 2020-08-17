import serial
from pygeocom import PyGeoCom

def main():
    ser = serial.Serial('/dev/ttyUSB0', 19200, timeout=1)
    
    geo = PyGeoCom(ser)

    r = geo.request(5003)
    print(r)
    ser.close()

if __name__ == "__main__":
    main()
