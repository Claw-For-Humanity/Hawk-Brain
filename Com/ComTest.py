import serial
import time

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

def write_read(x):
    arduino.write(bytes(x,'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
i= 0
while i <= 5:
    i += 1
    num = input('input number > ')
    value = write_read(num)
    print(value.decode('utf-8'))