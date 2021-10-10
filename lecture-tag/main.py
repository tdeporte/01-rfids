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

    #Le fast mode surveille constement les environs, il permet d'attendre l'arrivée d'un badge 
    os.write(rfid, b'\xFB')
    print("Fast mode active")
    
    while True:
        data = serie.read()
        if str(data)!= empty:
            #Boucle afin de récupérer l'ID du badge entier
            for i in range(12) :
                #Lit l'id d'un tag proche du récepteur 
                os.write(rfid, b'\xFA')
                data = serie.read()
                id+=str(data)[4:6]
                id+=':'
                #print(str(data))
            print(id)
            #Exit pour afficher les résultats clairement
            os.close(rfid)
            serie.close()
            sys.exit(0)

    

except KeyboardInterrupt:
    print("close")
    os.close(rfid)
    serie.close()