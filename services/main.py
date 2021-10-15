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

clients= {"00:00:b6:b7S:11:00:01:04:e0F:e6", "00:00]:a7:df:10:00:01:04:e0:12:d3"}

fast = 0

def init():
    os.write(rfid, b'\xFE')
    os.write(rfid, b'\xFC')

def open_door():
    print("Ouverture de la porte")
    time.sleep(1)
    print("Allumage LED verte")
    os.write(rfid, b'\xFF')
    time.sleep(3)
    print("Fermeture de la porte")
    time.sleep(1)
    print("Extinction LED verte")
    os.write(rfid, b'\xFE')

def match_clients(data):
    for i in clients:   
        if data==i:
            open_door()

def read_UID():
    os.write(rfid, b'\xFA')
    data = serie.read(12)

    data = str(data).replace('\\x', ':')
    data = data[3:len(data)-1]

    return data
        
try:
    
    init()

    while True:
        action = input("(1) Lire badge (doit être près du récepteur)\n(2) Activer Fast Mode\n(3) Quitter \n")
        
        if action == "1":
            print("Lecture du badge:")
            match_clients(read_UID())

        if action == "2":
            #Le fast mode surveille constamment les environs, il permet d'attendre l'arrivée d'un badge     
            print("Fast mode on")
            
            while True:
                data = read_UID()
                if str(data)!= empty:
                    match_clients(data)
                
        if action == "3":
            print("Extinction")
            os.close(rfid)
            serie.close()
            sys.exit(0)

        time.sleep(1)


except KeyboardInterrupt:
    print("close")
    os.close(rfid)
    serie.close()