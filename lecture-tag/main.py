import os, serial, time

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

    #Le fast mode surveille constement les environs, il permet d'attendre l'arrivée d'un badge 
    os.write(rfid, b'\xFB')
    print("Fast mode active")
    
    while True:
        os.write(rfid, b'\xFA')
        data = serie.read(12)

        if data != str.encode(''):
            print(data.decode("utf-8"))
            time.sleep(1)

    

except KeyboardInterrupt:
    print("close")
    os.close(rfid)
    serie.close()