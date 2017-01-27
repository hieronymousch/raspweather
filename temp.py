#coding: utf-8
import Adafruit_GPIO.I2C as I2C
import time
i2c = I2C
device=i2c.get_i2c_device(0x77) # address of BMP

# this value is necessary to calculate the correct height above sealevel
# its also included in airport wheather information ATIS named as QNH
# unit is hPa
QNH=1020

# power mode
# POWER_MODE=0 # sleep mode
# POWER_MODE=1 # forced mode
# POWER_MODE=2 # forced mode
POWER_MODE=3 # normal mode

# temperature resolution
# OSRS_T = 0 # skipped
# OSRS_T = 1 # 16 Bit
# OSRS_T = 2 # 17 Bit
# OSRS_T = 3 # 18 Bit
# OSRS_T = 4 # 19 Bit
OSRS_T = 5 # 20 Bit

# pressure resolution
# OSRS_P = 0 # pressure measurement skipped
# OSRS_P = 1 # 16 Bit ultra low power
# OSRS_P = 2 # 17 Bit low power
# OSRS_P = 3 # 18 Bit standard resolution
# OSRS_P = 4 # 19 Bit high resolution
OSRS_P = 5 # 20 Bit ultra high resolution

# filter settings
# FILTER = 0 #
# FILTER = 1 #
# FILTER = 2 #
# FILTER = 3 #
FILTER = 4 #
# FILTER = 5 #
# FILTER = 6 #
# FILTER = 7 #

# standby settings
T_SB = 0 # 000 0,5ms
# T_SB = 1 # 001 62.5 ms
# T_SB = 2 # 010 125 ms
# T_SB = 3 # 011 250ms
#T_SB = 4 # 100 500ms
# T_SB = 5 # 101 1000ms
# T_SB = 6 # 110 2000ms
# T_SB = 7 # 111 4000ms


CONFIG = (T_SB <<5) + (FILTER <<2) # combine bits for config
CTRL_MEAS = (OSRS_T <<5) + (OSRS_P <<2) + POWER_MODE # combine bits for ctrl_meas

# print ("CONFIG:",CONFIG)
# print ("CTRL_MEAS:",CTRL_MEAS)

BMP280_REGISTER_DIG_T1 = 0x88
BMP280_REGISTER_DIG_T2 = 0x8A
BMP280_REGISTER_DIG_T3 = 0x8C
BMP280_REGISTER_DIG_P1 = 0x8E
BMP280_REGISTER_DIG_P2 = 0x90
BMP280_REGISTER_DIG_P3 = 0x92
BMP280_REGISTER_DIG_P4 = 0x94
BMP280_REGISTER_DIG_P5 = 0x96
BMP280_REGISTER_DIG_P6 = 0x98
BMP280_REGISTER_DIG_P7 = 0x9A
BMP280_REGISTER_DIG_P8 = 0x9C
BMP280_REGISTER_DIG_P9 = 0x9E
BMP280_REGISTER_CHIPID = 0xD0
BMP280_REGISTER_VERSION = 0xD1
BMP280_REGISTER_SOFTRESET = 0xE0
BMP280_REGISTER_CONTROL = 0xF4
BMP280_REGISTER_CONFIG  = 0xF5
BMP280_REGISTER_STATUS = 0xF3
BMP280_REGISTER_TEMPDATA_MSB = 0xFA
BMP280_REGISTER_TEMPDATA_LSB = 0xFB
BMP280_REGISTER_TEMPDATA_XLSB = 0xFC
BMP280_REGISTER_PRESSDATA_MSB = 0xF7
BMP280_REGISTER_PRESSDATA_LSB = 0xF8
BMP280_REGISTER_PRESSDATA_XLSB = 0xF9

if (device.readS8(BMP280_REGISTER_CHIPID) == 0x58): # check sensor id 0x58=BMP280
    device.write8(BMP280_REGISTER_SOFTRESET,0xB6) # reset sensor
    time.sleep(0.2) # little break
    device.write8(BMP280_REGISTER_CONTROL,CTRL_MEAS) #
    time.sleep(0.2) # little break
    device.write8(BMP280_REGISTER_CONFIG,CONFIG)  #
    time.sleep(0.2)

    dig_T1 = device.readU16LE(BMP280_REGISTER_DIG_T1) # read correction settings
    dig_T2 = device.readS16LE(BMP280_REGISTER_DIG_T2)
    dig_T3 = device.readS16LE(BMP280_REGISTER_DIG_T3)
    dig_P1 = device.readU16LE(BMP280_REGISTER_DIG_P1)
    dig_P2 = device.readS16LE(BMP280_REGISTER_DIG_P2)
    dig_P3 = device.readS16LE(BMP280_REGISTER_DIG_P3)
    dig_P4 = device.readS16LE(BMP280_REGISTER_DIG_P4)
    dig_P5 = device.readS16LE(BMP280_REGISTER_DIG_P5)
    dig_P6 = device.readS16LE(BMP280_REGISTER_DIG_P6)
    dig_P7 = device.readS16LE(BMP280_REGISTER_DIG_P7)
    dig_P8 = device.readS16LE(BMP280_REGISTER_DIG_P8)
    dig_P9 = device.readS16LE(BMP280_REGISTER_DIG_P9)

    #while True: # loop
    raw_temp_msb=device.readU8(BMP280_REGISTER_TEMPDATA_MSB) # read raw temperature msb
    raw_temp_lsb=device.readU8(BMP280_REGISTER_TEMPDATA_LSB) # read raw temperature lsb
    raw_temp_xlsb=device.readU8(BMP280_REGISTER_TEMPDATA_XLSB) # read raw temperature xlsb
    raw_temp=(raw_temp_msb <<12)+(raw_temp_lsb<<4)+(raw_temp_xlsb>>4) # combine 3 bytes  msb 12 bits left, lsb 4 bits left, xlsb 4 bits right

    var1=(raw_temp/16384.0-dig_T1/1024.0)*dig_T2 # formula for temperature from datasheet
    var2=(raw_temp/131072.0-dig_T1/8192.0)*(raw_temp/131072.0-dig_T1/8192.0)*dig_T3 # formula for temperature from datasheet
    temp=(var1+var2)/5120.0 # formula for temperature from datasheet
    t_fine=(var1+var2) # need for pressure calculation

    print '{:.3f}'.format(temp)

