messages=[[[False,"Overlay launched.",(170,255,170)]]]
launched=[False]

old=print
def print(string):
   old("[Render] "+str(string))

def main():
   global messages
   global running
   fps = int(input("[2/3] Input desired FPS: "))
   div = float(input("[3/3] Resolution division (1 for fullscreen, 2 for half and so on): "))
   #fps = 60
   #div = 2
   import os
   from os import system
   import math
   import time
   from screeninfo import get_monitors
   from TwitchSocket import running
   from TaskHandler import TaskStep,tasks,taskCancels,KillTasks
   os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
   print("Importing pygame...")
   try:
      import pygame
   except ImportError:
      os.system('pip install pygame')
      import pygame
   mon = None
   for m in get_monitors():
      if m.is_primary:
         mon = m
         break
   launched[0]=True
   #ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
   resX=mon.width/div
   resY=mon.height/div
   pygame.font.init()
   font = pygame.font.SysFont('bahnschrift', math.floor(resY/36))
   twitch = pygame.image.load("twitch.png")
   imgoffset = resY/20
   twitch = pygame.transform.scale(twitch,(imgoffset,imgoffset))
   screen = pygame.display.set_mode((resX,resY))
   pygame.display.set_caption("Twitch Overlay")
   texts=[]
   textdata=[]
   def clamp(num, min_value, max_value):
       return max(min(num, max_value), min_value)
   def addText(msg):
      logo=msg[0]
      string=msg[1]
      color=msg[2]
      fnt=font.render(string,True,color)
      texts.append(fnt)
      textdata.append([fnt.get_height(),time.time(),logo])
   clock=pygame.time.Clock()
   running = True
   lastStep = 0
   tsFails=0
   while running:
       if lastStep != 0:
          try:
             TaskStep(lastStep)
          except Exception as ex:
             messages[0].append([False,"Could not TaskStep: "+str(ex),(255,0,0)])
             tsFails+=1
             if tsFails >= 5:
                tsFails=0
                messages[0].append([False,"Too many TaskStep errors! Clearing task list.",(170,170,255)])
                for i in range(len(taskCancels)):
                   KillTasks(i)
       for event in pygame.event.get():
           if event.type == 256:
               running=False
               break
       screen.fill((0,0,0))
       for i in range(len(messages[0])):
          print("Received "+messages[0][i][1])
          addText(messages[0][i])
       messages[0].clear()
       size = len(texts)
       toRemove1=[]
       toRemove2=[]
       for i in range(size):
           lifetime=clamp(time.time()-textdata[size-i-1][1]-5,0,2)
           if 255-(127*lifetime) <= 5:
               toRemove1.append(textdata[size-i-1])
               toRemove2.append(texts[size-i-1])
               #print("Removing "+str(size-i-1))
       for i in range(len(toRemove1)):
           textdata.remove(toRemove1[i])
       for i in range(len(toRemove2)):
           texts.remove(toRemove2[i])
       size = len(texts)
       for i in range(size):
           lifetime=clamp(time.time()-textdata[size-i-1][1]-5,0,2)
           o=imgoffset
           if textdata[size-i-1][2]:
              twitch.set_alpha(255-(127*lifetime))
              screen.blit(twitch,(0,resY-o*(i+1)))
           else:
              o=5
              pass
           texts[size-i-1].set_alpha(255-(127*lifetime))
           screen.blit(texts[size-i-1],(o,resY-(imgoffset)*(i+1)+(textdata[size-i-1][0]/2.5)))
       pygame.display.flip()
       lastStep=clock.tick(fps)/1000
