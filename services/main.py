import os, serial, time
import errno, sys
import json
import time 


empty = "b''"
clients = {"00:b6:b7:00:11:00:01:04:e0:00:e6:00:", "00:00:b1:00:11:00:01:04:e0:f9:87:00:", "00:00:a7:df:10:00:01:04:e0:12:d3:00:"}

f = open('services/data.json',"r")
data = json.load(f)

def str_match(str1,str2):
    #Retourne le pourcentage de corrélation entre deux string
    c = 0
    r = 0
    if len(str1)==len(str2):
        for i in range(len(str1)):
            if str1[i]==str2[i]:
                c+=1
        r = (c*100)/len(str1)
    return r

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
            id = ""
            #Boucle afin de récupérer l'ID du badge entier
            for i in range(12) :
                #Lit l'id d'un tag proche du récepteur 
                os.write(rfid, b'\xFA')
                data = serie.read()
                id+=str(data)[4:6]
                id+=':'
                #print(str(data))

            #print("Before regulation: "+id+"\n")
            #On remplit les trous dans l'ID par 00 par défaut
            for i in range(len(id)-1):
                if id[i]==id[i+1]==":":
                    id=id[:i+1]+"00"+id[i+1:]

            for i in clients:
                match = str_match(id,i)
                if match > 80:
                    print("Ouverture de la porte")


            #print("After regulation: "+id+"\n")
            #Exit pour afficher les résultats clairement
            #os.close(rfid)
            #serie.close()
            #sys.exit(0)
            #for i in data['clients']:
                
except KeyboardInterrupt:
    print("close")
    os.close(rfid)
    serie.close()