from os import system
from threading import Thread
print("[Main] Import Render.py")
from Render import main
print("[Main] Import TwitchSocket.py")
from TwitchSocket import *
import pydirectinput
start=time.time()
while True:
    #print("Starting PyGame thread...")
    thr=Thread(target=run)
    thr.start()
    while running[0]==False:
        time.sleep(0.1)
    thread=Thread(target=main)
    thread.start()
    while running[0]:
        if time.time()-start>60:
            start=time.time()
            pydirectinput.press('z')
        time.sleep(0.1)
    system('taskkill /f /im "python.exe"')
    
