import serial
from pygeocom import PyGeoCom, RecordFormat, ControllerMode, ControllerStopMode, LockInStatus, PrismType, ReflectorType, MeasurementMode, MeasurementProgram, TargetType, PositionMode, ATRRecognitionMode, OnOff
from datetime import datetime
from time import sleep, time

def main():
    ser = serial.Serial('/dev/ttyUSB0', 19200, timeout=180)
    
    geo = PyGeoCom(ser, debug = False)

    # print("Instrument Name: {}".format(geo.get_instrument_name()))
    # print("Serial Number:   {}".format(geo.get_instrument_number()))
    # print("Configuration")
    # print(geo.get_device_config())
    a, b, c = geo.get_software_version()
    print("Software Version: {}.{}.{}".format(a, b, c))
    a, b, c = geo.get_server_software_version()
    print("Server Software Version: {}.{}.{}".format(a, b, c))
    # print("Binary Protocol Available: {}".format('Yes' if geo.get_binary_available() else 'No'))
    # print()

    # a, b, c = geo.check_power()
    # print("Power Source: {} – Level: {}% – Action: {}".format(b, a, c))

    # print("Memory Voltage: {}V".format(geo.get_memory_voltage()))

    # print("Internal Temperature: {}°C".format(geo.get_internal_temperature()))

    # print("Date/Time")
    # print("Now:        {}".format(datetime.now()))
    # print("TPS Before: {}".format(geo.get_date_time()))
    # print("Setting time on TPS to now()")
    # geo.set_date_time(datetime.now())
    # print("TPS After:  {}".format(geo.get_date_time()))
    # print()

    # a, b = geo.get_up_counter()
    # print("Power On Cycles: {} – Wake-up Cycles: {}".format(a, b))

    #geo.local_mode()

    # a = geo.get_record_format()
    # print(a)
    #geo.set_record_format(RecordFormat.GSI_8 if a == RecordFormat.GSI_16 else RecordFormat.GSI_16)

    #geo.laser_pointer_on()
    #sleep(1)
    #geo.laser_pointer_off()
    #sleep(1)
    #geo.laser_pointer_on()
    #sleep(1)
    #geo.laser_pointer_off()

    #print(geo.get_egl_intensity())

    # print(geo.get_target_type())
    # print(geo.get_prism_type())

    # print(geo.get_prism_definition(PrismType.LEICA_ROUND))
    # print(geo.get_prism_definition(PrismType.LEICA_MINI))
    # print(geo.get_prism_definition(PrismType.LEICA_TAPE))
    # print(geo.get_prism_definition(PrismType.LEICA_360))
    # print(geo.get_prism_definition(PrismType.USER1))
    # print(geo.get_prism_definition(PrismType.USER2))
    # print(geo.get_prism_definition(PrismType.USER3))
    # print(geo.get_prism_definition(PrismType.LEICA_360_MINI))

    # For TPS1200 and onward I presume
    #print(geo.get_prism_definition(PrismType.MINI_ZERO))
    #print(geo.get_prism_definition(PrismType.USER))
    #print(geo.get_prism_definition(PrismType.HDS_TAPE))
    #print(geo.get_prism_definition(PrismType.GRZ121_ROUND))
    

    #print(geo.get_motor_lock_status())
    #geo.start_controller(ControllerMode.CONSTANT_SPEED)
    #print(geo.get_motor_lock_status())
    #geo.set_velocity(0.1, 0.1)
    #sleep(3)
    #geo.stop_controller(ControllerStopMode.NORMAL)
    #geo.start_controller(ControllerMode.RELATIVE_POSITIONING)

    # print(geo.get_measurement_program())

    #geo.set_measurement_program(MeasurementProgram.SINGLE_RLESS_VISIBLE)
    #print(geo.measure_distance_and_angles(MeasurementMode.DEFAULT_DISTANCE))

    #geo.set_target_type(TargetType.REFLECTOR)
    #geo.search_target()

    #print(geo.get_tolerance())
    #print(geo.get_positioning_timeout())

    #print(geo.measure_distance_and_angles(MeasurementMode.DEFAULT_DISTANCE))

    geo.position(2.736575413969699, 4.674161028769293, atr_mode = ATRRecognitionMode.TARGET)

    print(geo.measure_distance_and_angles(MeasurementMode.DEFAULT_DISTANCE))

    # geo.change_face(atr_mode = ATRRecognitionMode.TARGET)
    # print(geo.measure_distance_and_angles(MeasurementMode.DEFAULT_DISTANCE))

    print(geo.get_fine_adjust_mode())

    geo.fine_adjust(0.5, 0.5)
    print(geo.measure_distance_and_angles(MeasurementMode.DEFAULT_DISTANCE))

    geo.user_lock_state_on()
    geo.lock_in()
    sleep(10)
    geo.user_lock_state_off()

    ser.close()

if __name__ == "__main__":
    main()
