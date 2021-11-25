import serial
import time
# import math

COM = 'COM8'
port = serial.Serial(COM, 9600)
time.sleep(2)
value = [1358, 158, 2358, -9658]

while port.isOpen():
    comdata = int(input())
    if comdata == 0:
        for i in range(len(value)):
            port.write(str(value[i]).encode('ascii'))
            print(str(value[i]))
            time.sleep(0.02)
    else:
        while true:
            valor = port.readline().decode('ascii')
            print(valor)
            print("**********************")
