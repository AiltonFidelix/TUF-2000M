"""
Author: Ailton Fidelix
Date: 06/07/2021
Description: Modbus RTU communication test getting key records
"""

from time import sleep
import struct
import minimalmodbus
import serial

serialPort = '/dev/ttyUSB0'
flowMeterAddress = 1

instrument = minimalmodbus.Instrument(serialPort, flowMeterAddress)

instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.mode = minimalmodbus.MODE_RTU
instrument.debug = False


def readFloatReg(regOne, regTwo):
    data = (instrument.read_register(
        regOne), instrument.read_register(regTwo))
    packed_string = struct.pack("HH", *data)
    unpacked_string = struct.unpack("f", packed_string)[0]
    return float("{:.2f}".format(unpacked_string))


def readLongReg(regOne, regTwo):
    return ((instrument.read_register(regTwo) << 0) & 0xFFFF) + \
        ((instrument.read_register(regOne) << 16))


def readFlow():
    print(f'Flow rate: {readFloatReg(1, 2)} m3/h')


def readEnergyFlow():
    print(f'Energy flow rate: {readFloatReg(3, 4)} GJ/h')


def readVelocity():
    print(f'Velocity: {readFloatReg(5, 6)} m/s')


def readFluidSoundSpeed():
    print(f'Fluid sound speed: {readFloatReg(7, 8)} m/s')


def readNetAccumulator():
    print(f'Net accumulator: {readLongReg(25, 26)}')


def readError():
    print(f'Error: {instrument.read_register(72)}')


def readWorkTime():
    seconds = readLongReg(103, 104)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print(f'Work time: {"%d:%02d:%02d" % (h, m, s)}')


def readOnOffTotal():
    print(f'Total power on-off: {readLongReg(105, 106)}')


def readStreamStrength():
    print(f'Upstream: {instrument.read_register(93)} Downstream: {instrument.read_register(94)}')


def readSignalQuality():
    print(f'Signal quality: {instrument.read_register(92)}')



if __name__ == '__main__':

    print('*-------------------------------------------------------------*')
    print('                  Ultrassonic Flow Meter                       ')
    print('                       TUF-2000M                               ')
    print('                    Communication test                         ')
    print('*-------------------------------------------------------------*')

    while True:
        sleep(1)
        readFlow()
        readEnergyFlow()
        readVelocity()
        readFluidSoundSpeed()
        readNetAccumulator()
        readStreamStrength()
        readWorkTime()
        readOnOffTotal()
        readSignalQuality()
        readError()
        print('*-------------------------------------------------------------*')
