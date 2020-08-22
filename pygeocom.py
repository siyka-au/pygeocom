from typing import Tuple, Any
from enum import Enum, IntFlag
from datetime import datetime

class TargetType(Enum):
    REFLECTOR = 0
    REFLECTORLESS = 1

class InclinationSensorProgram(Enum):
    TMC_MEA_INC = 0     # Use sensor (apriori sigma)
    TMC_AUTO_INC = 1    # Automatic mode (sensor/plane)
    TMC_PLANE_INC = 2   # Use plane (apriori sigma)

class TMCMeasurementMode(Enum):
    TMC_STOP = 0            # Stop measurement program
    TMC_DEF_DIST = 1        # Default DIST-measurement program
    TMC_TRK_DIST = 2        # Distance-TRK measurement program
    TMC_CLEAR = 3           # TMC_STOP and clear data
    TMC_SIGNAL = 4          # Signal measurement (test function)
    TMC_DO_MEASURE = 6      # (Re)start measurement task
    TMC_RTRK_DIST = 8       # Distance-TRK measurement program
    TMC_RED_TRK_DIST = 10   # Red laser tracking
    TMC_FREQUENCY = 11      # Frequency measurement (test)

class EdmMode(Enum):
    EDM_MODE_NOT_USED = 0   # Init value
    EDM_SINGLE_TAPE = 1     # Single measurement with tape
    EDM_SINGLE_STANDARD = 2 # Standard single measurement
    EDM_SINGLE_FAST = 3     # Fast single measurement
    EDM_SINGLE_LRANGE = 4   # Long range single measurement
    EDM_SINGLE_SRANGE = 5   # Short range single measurement
    EDM_CONT_STANDARD = 6   # Standard repeated measurement
    EDM_CONT_DYNAMIC = 7    # Dynamic repeated measurement
    EDM_CONT_REFLESS = 8    # Reflectorless repeated measurement
    EDM_CONT_FAST = 9       # Fast repeated measurement
    EDM_AVERAGE_IR = 10     # Standard average measurement
    EDM_AVERAGE_SR = 11     # Short range average measurement
    EDM_AVERAGE_LR = 12     # Long range average measurement

class DeviceClass(Enum):
    # TPS1000 Family        ------------------------ accuracy
    TPS_CLASS_1100 = 0      # TPS1000 family member, 1 mgon,   3"
    TPS_CLASS_1700 = 1      # TPS1000 family member, 0.5 mgon, 1.5"
    TPS_CLASS_1800 = 2      # TPS1000 family member, 0.3 mgon, 1"
    TPS_CLASS_5000 = 3      # TPS2000 family member
    TPS_CLASS_6000 = 4      # TPS2000 family member 
    TPS_CLASS_1500 = 5      # TPS1000 family member
    TPS_CLASS_2003 = 6      # TPS2000 family member
    TPS_CLASS_5005 = 7      # TPS5000      "
    TPS_CLASS_5100 = 8      # TPS5000      "

    # TPS1100 Family        ------------------------ accuracy
    TPS_CLASS_1102 = 100    # TPS1000 family member, 2"
    TPS_CLASS_1103 = 101    # TPS1000 family member, 3"
    TPS_CLASS_1105 = 102    # TPS1000 family member, 5"
    TPS_CLASS_1101 = 103    # TPS1000 family member, 1."

    # TPS1200 Family        ------------------------ accuracy
    TPS_CLASS_1202 = 200    # TPS1200 family member, 2"
    TPS_CLASS_1203 = 201    # TPS1200 family member, 3"
    TPS_CLASS_1205 = 202    # TPS1200 family member, 5"
    TPS_CLASS_1201 = 203    # TPS1200 family member, 1"

class DeviceType(IntFlag):
    # TPS1x00 common
    TPS_DEVICE_T   = 0x00000   # Theodolite without built-in EDM
    TPS_DEVICE_MOT = 0x00004   # Motorized device
    TPS_DEVICE_ATR = 0x00008   # Automatic Target Recognition
    TPS_DEVICE_EGL = 0x00010   # Electronic Guide Light
    TPS_DEVICE_DB  = 0x00020   # reserved (Database, not GSI)
    TPS_DEVICE_DL  = 0x00040   # Diode laser
    TPS_DEVICE_LP  = 0x00080   # Laser plumbed

    # TPS1000 specific
    TPS_DEVICE_TC1 = 0x00001   # tachymeter (TCW1)
    TPS_DEVICE_TC2 = 0x00002   # tachymeter (TCW2)

    # TPS1100/TPS1200 specific
    TPS_DEVICE_TC     = 0x00001 # tachymeter (TCW3)
    TPS_DEVICE_TCR    = 0x00002 # tachymeter (TCW3 with red laser)
    TPS_DEVICE_ATC    = 0x00100 # Autocollimation lamp (used only PMU)
    TPS_DEVICE_LPNT   = 0x00200 # Laserpointer
    TPS_DEVICE_RL_EXT = 0x00400 # Reflectorless EDM with extended range (Pinpoint R100,R300)
    TPS_DEVICE_PS     = 0x00800 # Power Search

    # TPSSim specific
    TPS_DEVICE_SIM = 0x04000     # runs on Simulation, no Hardware

class PowerPath(Enum):
    CURRENT_POWER = 0
    EXTERNAL_POWER = 1
    INTERNAL_POWER = 2

class RecordFormat(Enum):
    GSI_8  = 0
    GSI_16 = 1

class TpsStatus(Enum):
    OFF = 0
    SLEEPING = 1
    ONLINE = 2
    LOCAL = 3
    UNKNOWN = 4

class byte(int):
    def __new__(cls, value, *args, **kwargs):
        if (type(value) == str):
            value = int(value.strip("'"), 16)
        elif (type(value) == bytes):
            value = int(value.strip(b"'"), 16)
        
        if value < 0:
            raise ValueError("byte types must not be less than zero")
        if value > 255:
            raise ValueError("byte types must not be more than 255 (0xff)")
        
        return  super(cls, cls).__new__(cls, value)

class PyGeoCom:
    def __init__(self, stream):
        self.__stream = stream
        self.__stream.write(b'\n')

    def __request(self, rpc_id: int, args: Tuple[Any, ...] = ()) -> Tuple[Any, ...]:

        def encode(arg) -> str:
            if (type(arg) == str):
                return '"{}"'.format(arg)
            elif (type(arg) == int):
                return '{}'.format(arg)
            elif (type(arg) == float):
                return '{}'.format(arg)
            elif (type(arg) == byte):
                return "'{:02X}'".format(arg)

        d = '\n%R1Q,{}:{}\r\n'.format(rpc_id, ','.join([encode(a) for a in args])).encode('ascii')
        #print(b'>> ' + d)
        self.__stream.write(d)

        d = self.__stream.readline()
        #print(b'<< ' + d)
        header, parameters = d.split(b':', 1)
        
        reply_type, geocom_return_code, transaction_id = header.split(b',')
        assert reply_type == b'%R1P'
        geocom_return_code = int(geocom_return_code)
        transaction_id = int(transaction_id)

        parameters = parameters.rstrip()
        rpc_return_code, *parameters = parameters.split(b',')
        rpc_return_code = int(rpc_return_code)
        assert rpc_return_code == 0
        
        return parameters

    def get_instrument_number(self) -> int:
        instrument_number, = self.__request(5003)
        return int(instrument_number)

    def get_instrument_name(self) -> str:
        instrument_name, = self.__request(5004)
        return instrument_name.decode('utf-8').strip('"')

    def get_device_config(self) -> DeviceType:
        device_class, device_type = self.__request(5035)
        return DeviceClass(int(device_class)), DeviceType(int(device_type))

    def get_date_time(self) -> datetime:
        year, month, day, hour, minute, second = self.__request(5008)
        year = int(year)
        month = byte(month)
        day = byte(day)
        hour = byte(hour)
        minute = byte(minute)
        second = byte(second)
        return datetime(year, month, day, hour, minute, second)
    
    def set_date_time(self, dt: datetime):
        self.__request(5007, (dt.year, byte(dt.month), byte(dt.day), byte(dt.hour), byte(dt.minute), byte(dt.second)))

    def get_software_version(self) -> (int, int, int):
        release, version, subversion = self.__request(5034)
        return int(release), int(version), int(subversion)

    def check_power(self) -> (int, PowerPath, PowerPath):
        capacity, active_power, power_suggest = self.__request(5039)
        return int(capacity), PowerPath(int(active_power)), PowerPath(int(power_suggest))

    def get_memory_voltage(self) -> float:
        memory_voltage, = self.__request(5010)
        return float(memory_voltage)

    def get_internal_temperature(self) -> float:
        internal_temperature, = self.__request(5011)
        return float(internal_temperature)

    def get_up_counter(self) -> (int, int):
        power_on, wake_up = self.__request(12003)
        return int(power_on), int(wake_up)

    def get_binary_available(self) -> bool:
        binary_available, = self.__request(113)
        return bool(binary_available)

    def local_mode(self):
        self.__request(1)

    def get_record_format(self) -> RecordFormat:
        record_format, = self.__request(8011)
        return RecordFormat(int(record_format)),

    def set_record_format(self, record_format: RecordFormat):
        self.__request(8012, (record_format.value,))

    def get_double_precision_setting(self) -> int:
        number_of_digits, = self.__request(108)
        return int(number_of_digits)

    def set_double_precision_setting(self, number_of_digits: int):
        if number_of_digits < 0:
            raise ValueError("Number of digits must be greater than or equal to 0")
        if number_of_digits > 15:
            raise ValueError("Number of digits must be lesser than or equal to 15")
        self.__request(107, (number_of_digits,))