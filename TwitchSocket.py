import time
import random
import datetime
import math
try:
   import websocket
except ImportError:
   from os import system
   system('pip install websocket-client')
   import websocket
from threading import Thread
from Render import messages,launched
from TaskHandler import tasks,addTask

success=False
nonce = ""
running=[False]
old=print
def print(string):
   old("[TwitchSocket] "+str(string))

#channel = input("[1/3] Input name of account to track: ")
channel = "EmK530"
start = time.time()
firstrun = True
file=open("auth.txt","r")
account=file.readlines()
file.close()
new=[]
m=account
for i in range(len(m)):
   new.append(m[i].replace("\n",""))
account=new
print("Successfully loaded authentication file for '"+account[2].split("NICK ")[1]+"'")
channel=channel.lower()
def write(string):
   global messages
   messages.append(string)

def send_message(ws, msg):
   global nonce
   ws.send("@client-nonce="+nonce+" PRIVMSG #"+channel+" :"+msg)
comms=["jump","spin","longjump","camleft","camright","dive",
       "backflip","w","a","s","d","pound","camup","camdown",
       "stop","dance","dab","djump","backflipw","crouch","pause",
       "follow","bth","snapshoot","makebth"
]
instComms=["spin","dive","backflip","pound","stop","dance","pause","follow","bth","snapshoot","makebth"]
def handle_message(ws, msg, name):
   global send_message
   upName=name
   ogMsg=msg
   msg=msg.lower()
   name=name.lower()
   if msg[0:1]== "!":
      write(name+": "+msg)
      com=msg.split("!")[1].split(" ")
      dur=None
      if len(com)!=1:
         dur=com[1]
      com=com[0]
      if com=="uptime":
         send_message(ws, "I have been online for "+str(datetime.timedelta(seconds=math.floor(time.time()-start))))
      elif com=="help":
         send_message(ws, "Commands can be found at: https://blog.emk530.net/tpr64")
      elif com in comms:
         idx=comms.index(com)
         if com in instComms:
            dur=None
         try:
            addTask(idx,dur,upName)
         except Exception as ex:
            messages[0].append([False,"Could not addTask: "+str(ex),(255,0,0)])
   else:
      messages[0].append([True,upName+": "+ogMsg,(255,255,255)])

def on_message(ws, message):
   global success
   global launched
   global lifetime
   global nonce
   global write
   global handle_message
   global running
   global firstrun
   #print(message)
   if "Welcome, GLHF!" in message:
      ws.send("JOIN #"+channel+"")
      #print("Client welcomed, joining channel")
      print("Twitch connection opened!")
      if not firstrun:
         ws.send("@client-nonce="+nonce+" PRIVMSG #"+channel+" :"+"Bot has recovered from a connection error.")
      running[0] = True
      nonce = ("%032x" % random.getrandbits(128))
      #ws.send("@client-nonce="+nonce+" PRIVMSG #"+channel+" :"+"Server is now online, hello world!")
   elif "client-nonce=" in message and message.split("client-nonce=")[1].split(";")[0] != nonce:
      msg = message.split("PRIVMSG")[1].split(":")[1].split("\r")[0]
      name = message.split("display-name=")[1].split(";")[0]
      handle_message(ws,msg,name)
   elif "NOTICE" in message:
      msg=message.split("NOTICE")[1].split(":")[1]
      print("NOTICE: "+msg)
   elif "authentication failed" in message:
      print("Login failed.")
      ws.close()
   elif "PING" in message:
      if launched[0]:
         print("Twitch PING PONG")
      ws.send("PONG")

def on_error(ws, error):
   print("ERROR! '"+str(error)+"'")
   running[0] = False
   ws.close()

def on_close(ws,a,b):
   global firstrun
   firstrun = False
   #print("Connection closed")

def on_open(ws):
   global firstrun
   print("Authenticating...")
   for i in range(4):
      ws.send(account[i])
   #ws.send('CAP REQ :twitch.tv/tags twitch.tv/commands')
   #ws.send('PASS SCHMOOPIIE')
   #ws.send('NICK justinfan16911')
   #ws.send('USER justinfan16911 8 * :justinfan16911')
   #print("Login sent")
def run():
   if True:
      while True:
         print("Connecting to Twitch...")
         websocket.enableTrace(False)
         ws = websocket.WebSocketApp("wss://irc-ws.chat.twitch.tv/",
         on_message = on_message,
         on_error = on_error,
         on_close = on_close,
         header = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'Upgrade',
            'Pragma': 'no-cache',
            'Host': 'irc-ws.chat.twitch.tv',
            'Origin': 'https://www.twitch.tv',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
         })
         ws.on_open = on_open
         ws.run_forever()
   else:
      running[0] = True
      print("Connection cancelled.")
