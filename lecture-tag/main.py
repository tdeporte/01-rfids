import os, serial, time
import errno, sys

id = ""
empty = "b''"
try:
    device = '/dev/ttyUSB0'

    rfid = os.open(device, os.O_RDWR)
    serie = serial.Serial(
        device,
        19200, 
        timeout=1,
        bytesize=serial.EIGHTBITS, 
        parity=serial.PARITY_NONE, 
        stopbits=serial.STOPBITS_ONE)
    
    while True:
        os.write(rfid, b'\xFA')
        data = serie.read(12)
        
        if str(data)!= empty:
            data = str(data).replace('\\x', ':')
            data = data[3:len(data)-1]
            print(data)
            time.sleep(1)

except KeyboardInterrupt:
    print("close")
    os.close(rfid)
    serie.close()