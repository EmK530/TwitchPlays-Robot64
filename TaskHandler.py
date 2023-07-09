import pydirectinput,math
from Render import messages

pydirectinput.PAUSE = 0

old=print
def print(string):
   old("[TaskHandler] "+str(string))
tasks = [[]]
defaultTaskLength=[0.25,None,1,45,45,None,None,1,1,1,1,None,22.5,22.5,0.25,None,1,0.5,1.5,1,None,None,None,None,None]
taskLengthLimit=[30,None,3,180,180,None,None,10,10,10,10,None,90,90,0.25,None,10,1,3,10,None,None,None,None,None]
f={
   "keyDown":pydirectinput.keyDown,
   "keyUp":pydirectinput.keyUp,
   "press":pydirectinput.press,
   "click":pydirectinput.click
}
taskNames=(
   "Jump","Spin Attack","Long Jump","Camera Left","Camera Right",
   "Dive [E]","Backflip","Move Forward","Move Left","Move Backwards","Move Right",
   "Ground Pound","Camera Up","Camera Down","Stop Moving","Dance","Dab","Double Jump",
   "Backflip Forwards","Crouch","Pause","Follow Camera","Back to Hub","Snapshoot","MAKE Back to Hub"
)
taskUnit=(
   "sec",None,"sec","degrees","degrees",None,None,"sec","sec","sec","sec",None,"degrees","degrees",None,None,
   "sec","sec Delay","sec","sec",None,None,None,None,None
)
taskButtons=[
   ['space'],
   ['shiftright'],
   [[
      ['w','keyDown'],
      ['shift','keyDown'],
      ['space','press'],
      ['shift','keyUp']
   ],[
      ['w','keyUp']
   ]],
   ['left'],
   ['right'],
   ['e'],
   [[
      ['shift','keyDown'],
      ['space','press'],
      ['shift','keyUp']
   ]],
   ['w'],
   ['a'],
   ['s'],
   ['d'],
   [[
      ['space','press'],
      ['shift','press']
   ]],
   ['up'],
   ['down'],
   [[
      ['shift','keyDown']
   ],[
      ['shift','keyUp']
   ]],
   ['ctrl'],
   ['enter'],
   [[
      ['space','press']
   ],[
      ['space','press']
   ]],
   [[
      ['shift','keyDown'],
      ['space','press'],
      ['shift','keyUp'],
      ['w','keyDown']
   ],[
      ['w','keyUp']
   ]],
   [[
      ['shift','keyDown']
   ],[
      ['shift','keyUp']
   ]],
   ['p'],
   [[
      [(769,669),'moveTo'],
      [None,'click']
   ]],
   [[
      [(789,756),'moveTo'],
      [None,'click'],
      [(777,317),'moveTo'],
      [None,'click']
   ]],
   [[
      [(774,492),'moveTo'],
      [None,'click'],
      ['e','press']
   ]],
   [[
      [(1276,97),'moveTo'],
      [None,'click'],
      ['shiftright','press'],
      ['p','press'],
      [(789,756),'moveTo'],
      [None,'click'],
      [(777,317),'moveTo'],
      [None,'click']
   ]]
]
taskCancels=[
   [0,17],
   None,
   [2,7],
   None,
   None,
   None,
   None,
   [2,7,18],
   [8],
   [9],
   [10],
   None,
   None,
   None,
   [2,7,8,9,10,17,18,19],
   None,
   None,
   [0,17],
   [7,18],
   [14,17,19],
   None,
   None,
   None,
   None,
   None
]
pause=False
UIdeb=False
multiTask = [False,False,True,False,False,False,True,False,False,False,False,True,False,False,True,False,False,True,True,True,False,True,True,True,True]
camTask = [False,False,False,True,True,False,False,False,False,False,False,False,True,True,False,False,False,False,False,False,False,False,False,False,False]
UITask = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,True,True,True,False]
UIdebL = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,True,True,True]
def KillTasks(taskId):
   nonunique=False
   for i in tasks[0]:
      if taskId == i[0]:
         print("Killed task ID "+str(i[0]))
         if not nonunique:
            nonunique=True
            if not multiTask[i[0]]:
               TaskPress(taskButtons[i[0]],"keyUp")
            else:
               TaskHandleMulti(taskButtons[i[0]],1,i[0])
         tasks[0].remove(i)
def TaskPress(li,func):
   for a in li:
      f[func](a)
def TaskHandleMulti(li,idx,taskId):
   global UIdeb,pause
   pydirectinput.PAUSE = 1/60
   for a in li[idx]:
      if a[1]=="moveTo":
         pydirectinput.moveTo(a[0][0],a[0][1])
         pydirectinput.move(1,0)
      elif a[1]=="click":
         pydirectinput.click()
      else:
         f[a[1]](a[0])
   pydirectinput.PAUSE = 0
   UIdeb=False
   if taskNames[taskId]=="Back to Hub":
      pause=False
   elif taskNames[taskId]=="MAKE Back to Hub":
      pause=False
def addTask(taskId, duration, user):
   global pause,UIdeb
   if not duration:
      duration = defaultTaskLength[taskId]
   else:
      try:
         duration = float(duration)
      except Exception:
         duration = defaultTaskLength[taskId]
   if duration!=None and math.isnan(duration):
      duration = defaultTaskLength[taskId]
   if duration!=None and duration > taskLengthLimit[taskId]:
      duration = taskLengthLimit[taskId]
      print(duration)
   oldDur=duration
   if camTask[taskId]:
      duration/=188
   tc=taskCancels[taskId]
   if tc!=None:
      for i in tc:
         KillTasks(i)
   #print("Received task ID "+str(taskId)+", duration: "+str(duration))
   if taskNames[taskId]=="Pause":
      pause=not pause
   msg=user+": "+str(taskNames[taskId])
   if duration!=None and duration>0 and taskUnit[taskId]!=None:
      msg=msg+" ("+str(oldDur)+" "+str(taskUnit[taskId])+")"
   if not UIdeb and ((pause and UITask[taskId]) or (not pause and not UITask[taskId]) or taskNames[taskId]=="Pause"):
      messages[0].append([True,msg,(170,255,170)])
      tasks[0].append([taskId,duration,False])
      UIdeb=UIdebL[taskId]
   else:
      messages[0].append([True,msg,(255,170,170)])
   
def TaskStep(dt):
   for i in tasks[0]:
      check=True
      if not i[2]:
         i[2]=True
         if not multiTask[i[0]]:
            if i[1] != None:
               TaskPress(taskButtons[i[0]],"keyDown")
            else:
               TaskPress(taskButtons[i[0]],"press")
         else:
            TaskHandleMulti(taskButtons[i[0]],0,i[0])
      else:
         i[1]-=dt
      if i[1] == None:
         check=False
         tasks[0].remove(i)
      if check:
         if i[1]<=0:
            if not multiTask[i[0]]:
               TaskPress(taskButtons[i[0]],"keyUp")
            else:
               TaskHandleMulti(taskButtons[i[0]],1,i[0])
            tasks[0].remove(i)
