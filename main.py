import serial
from pygeocom import PyGeoCom, RecordFormat, ControllerMode, ControllerStopMode, LockInStatus
from datetime import datetime
from time import sleep, time

def main():
    ser = serial.Serial('/dev/ttyUSB0', 19200, timeout=1)
    
    geo = PyGeoCom(ser)

    print("Instrument Name: {}".format(geo.get_instrument_name()))
    print("Serial Number:   {}".format(geo.get_instrument_number()))
    print("Configuration")
    print(geo.get_device_config())
    a, b, c = geo.get_software_version()
    print("Software Version: {}.{}.{}".format(a, b, c))
    print("Binary Protocol Available: {}".format('Yes' if geo.get_binary_available() else 'No'))
    print()

    a, b, c = geo.check_power()
    print("Power Source: {} – Level: {}% – Action: {}".format(b, a, c))

    print("Memory Voltage: {}V".format(geo.get_memory_voltage()))

    print("Internal Temperature: {}°C".format(geo.get_internal_temperature()))

    print("Date/Time")
    print("Now:        {}".format(datetime.now()))
    print("TPS Before: {}".format(geo.get_date_time()))
    print("Setting time on TPS to now()")
    geo.set_date_time(datetime.now())
    print("TPS After:  {}".format(geo.get_date_time()))
    print()

    a, b = geo.get_up_counter()
    print("Power On Cycles: {} – Wake-up Cycles: {}".format(a, b))

    #geo.local_mode()

    a = geo.get_record_format()
    print(a)
    #geo.set_record_format(RecordFormat.GSI_8 if a == RecordFormat.GSI_16 else RecordFormat.GSI_16)

    #geo.laser_pointer_on()
    #sleep(1)
    #geo.laser_pointer_off()
    #sleep(1)
    #geo.laser_pointer_on()
    #sleep(1)
    #geo.laser_pointer_off()

    #print(geo.get_egl_intensity())

    print(geo.get_motor_lock_status())


    geo.start_controller(ControllerMode.LOCK_IN)

    timeout = 5   # [seconds]
    timeout_start = time()

    while time() < timeout_start + timeout:
        if geo.get_motor_lock_status() == LockInStatus.LOCKED_IN:
            break

    print(geo.get_motor_lock_status())

    geo.stop_controller(ControllerStopMode.NORMAL)

    print(geo.get_motor_lock_status())

    ser.close()

if __name__ == "__main__":
    main()
