import warnings
import panel as pn
import pathlib
import logging
import time
import numpy as np
from matplotlib import pyplot as plt

from game.window import Game
import pygame

from threading import Thread
import brainaccess_board as bb
from brainaccess_board.utils import find_free_port

def calc_move():
    data = db.get_mne(duration=5)
    if not data:
        return
    k2=data[devices[0]].get_data()[2]
    k4=data[devices[0]].get_data()[3]

    ruch(k2,k4)

game = Game(calc_move)


def ruch1(k2,k4, sredniak4, sredniak2):
    indeks = np.argmax(k4)
    ppK4 = np.max(k4) - np.min(k4)
    ppK2 = np.max(k2) - np.min(k2)
    
    print(ppK4)
    print(ppK2)

    if ppK4 > 0.01 and ppK2 > 0.01:
        print("Strzał")
    if ppK4 > 0.01:
        print("Prawo")
    if ppK2 > 0.01:
        print("Lewo")
    
    print("nic")


def ruch2(k2,k4, sredniak4, sredniak2):
    indeks = np.argmax(k4)
    print(f'maxk4: {np.max(k4)}')
    print(f'roznica: {np.max(k4) - sredniak4}')
    print(f'maxk2indeks: {k2[indeks]}')
    print(f'roznicak2: {k2[indeks] - sredniak2}')
    
    if np.max(k4) - k2[indeks] <=0.011270443359375:
         
        print("strzal") 
    if np.max(k4) - sredniak4 >=0.52 and k2[indeks] - sredniak2 <0.52: 
        print("lewo") 
    if np.max(k2) - sredniak2 >=0.52 and k4[indeks] - sredniak4 <0.52: 
        print("prawo")
    
    print("nic")

def ruch(k2,k4):
    indeks = np.argmax(k4)
    sredniak2= np.mean(k2)
    sredniak4 = np.mean(k4)
    print(f'sredniak2: {sredniak2} sredniak4: {sredniak4}'  ) 
    print(f'max4 - indeksk2: {np.max(k4) - k2[indeks]}')
    print(f'maxk4: {np.max(k4)}')
    print(f'roznica: {np.max(k4) - sredniak4}')
    print(f'maxk2indeks: {k2[indeks]}')
    print(f'roznicak2: {k2[indeks] - sredniak2}')
    
    print(f'maxk2: {np.max(k2)}')
    print(f'roznicak2: {np.max(k2) - sredniak2}')
    print(f'maxk4indeks: {k4[indeks]}')
    print(f'roznicak4: {k4[indeks] - sredniak4}')
    
    if np.max(k4) - k2[indeks] <=0.0448702109375:
        print("strzal")
        game.player_shoot() 


    if np.max(k4) - sredniak4 >=0.0007060695234374914 and k2[indeks] - sredniak2 <= 0.0013156796234375032: 
        print("lewo") 
        game.player_left()

    if np.max(k2) - sredniak2 >=-0.0033835281064356487 and k4[indeks] - sredniak4 <=0.0005946892728960415: 
        print("prawo")
        game.player_right()



    if np.max(k4) - sredniak4 <=0.0003381004146039632 and np.max(k2) - sredniak2 <= 0.0003184377289603829:
        print("nic")

db, db_status = bb.db_connect()
if not db_status:
    raise Exception("Database connection failed")


data = db.get_mne(duration=20)

devices = list(data.keys())
sredniak2= np.mean(data[devices[0]].get_data()[2])
sredniak4 = np.mean(data[devices[0]].get_data()[3])
print(sredniak2, sredniak4)


k2=data[devices[0]].get_data()[2]
k4=data[devices[0]].get_data()[3]

game.run()

