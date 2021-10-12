import os, serial, time
import errno, sys
import json
import time 
import re

device = '/dev/ttyUSB0'
rfid = os.open(device, os.O_RDWR)
serie = serial.Serial(
        device,
        19200, 
        timeout=1,
        bytesize=serial.EIGHTBITS, 
        parity=serial.PARITY_NONE, 
        stopbits=serial.STOPBITS_ONE)

empty = "b''"
clients = {"00:00:b6:b7:00:11:00:01:04:e0:00:e6:", "00:00:00:b1:00:11:00:01:04:e0:f9:87:", "00:00:00:a7:df:10:00:01:04:e0:12:d3:"}
clients_fast_mode = {"00:b6:b7:00:11:00:01:04:e0:00:e6:00:", "00:00:b1:00:11:00:01:04:e0:f9:87:00:", "00:00:a7:df:10:00:01:04:e0:12:d3:00:"}

f = open('services/data.json',"r")
data = json.load(f)

fast_mode = False

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

def init():
    os.write(rfid, b'\xFE')
    os.write(rfid, b'\xFC')

def fill_holes(id):
    for i in range(len(id)-1):
        if id[i]==id[i+1]==":":
            id=id[:i+1]+"00"+id[i+1:]
    return id

def read_UID():
    id = ""
    #Boucle afin de récupérer l'ID du badge entier
    for i in range(12) :
        #Lit l'id d'un tag proche du récepteur 
        os.write(rfid, b'\xFA')
        data = serie.read()
        id+=str(data)[4:6]
        id+=':'
        #print(str(data))

    #On remplit les trous dans l'ID par 00 par défaut
    id = fill_holes(id)
    #print(id)

    liste_clients = clients
    if fast_mode == True:
        liste_clients = clients_fast_mode

    for i in liste_clients:   
        match = str_match(id,i)
        #print(id)
        #print(i)
        #print(match)
        if match > 90:
            print("Ouverture de la porte")
            time.sleep(1)
            os.write(rfid, b'\xFF')
            time.sleep(3)
            print("Fermeture de la porte")
            os.write(rfid, b'\xFE')


def fast_mode():
    
    #Le fast mode surveille constamment les environs, il permet d'attendre l'arrivée d'un badge 
    os.write(rfid, b'\xFB')
    fast_mode=True
    print("Fast mode on")
    
    while True:
        data = serie.read()
        if str(data)!= empty:
            read_UID()

try:
    
    init()

    while True:
        action = input("(1) Lire badge (doit être près du récepteur)\n(2) Activer Fast Mode\n(3) Quitter \n")
        
        if action == "1":
            print("Lecture :")
            read_UID()

        if action == "2":
            fast_mode()
        
        if action == "3":
            print("close")
            os.close(rfid)
            serie.close()
            sys.exit(0)

        time.sleep(1)


except KeyboardInterrupt:
    print("close")
    os.close(rfid)
    serie.close()