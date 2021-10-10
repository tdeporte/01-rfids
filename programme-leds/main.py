import os, serial, time

device = '/dev/ttyUSB0'

rfid = os.open(device, os.O_RDWR)
serie = serial.Serial(device, 19200, timeout=1)

os.write(rfid, b'\xFD')
print("LED rouge allumÃ©e")

delay = 3
print("Attente de", delay, "seconde(s)")
time.sleep(delay)

os.write(rfid, b'\xFC')
print("LED rouge Ã©teinte")

os.close(rfid)
serie.close()