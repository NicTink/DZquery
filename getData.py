print("loading...")
import getInfo, getIpPort, time, socket, sys, json, tkinter, win32api, win32con, pywintypes, threading, os, watchdogLocal, keybindsLocal
from ctypes import *


config={
  "config": {
	"updateRate": 60,
	"PfromTop": "1000",
	"PfromSide": "1720",
	"TextColour": "green",
	"BGColour": "black"
  }
}
exists = os.path.isfile('./config/config.json')
if not os.path.exists("./config/"):
	os.makedirs("./config/")
if exists==False:
	print("config.json missing... creating")
	with open('./config/config.json', 'w') as outfile:
		json.dump(config, outfile)



print("system prepared")

STD_OUTPUT_HANDLE = -11
 
class COORD(Structure):
	pass
 
COORD._fields_ = [("X", c_short), ("Y", c_short)]
 
def print_at(r, c, s):
	h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
	windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
 
	c = s.encode("windows-1252")
	windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)


def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# doesn't even have to be reachable
		s.connect(('10.255.255.255', 1))
		IP = s.getsockname()[0]
	except:
		IP = '127.0.0.1'
		#no internet connection
		print("OOPS! It looks like you dont have internet connection")
	finally:
		s.close()
	return IP
global i

def refreshStats(label):
	print("loading...")
	label.config(text="loading...")
	import getGameServer
	sys.stdout.write("waiting for server connection...	 ")
	label.config(text="waiting connection...")
	sys.stdout.flush()
	localip= str(get_ip())
	IPPORT=[localip,2304]
	IPPORTref=[localip,2304]
	'''
	#for testing!
	IPPORT=["64.95.100.142",2402]
	'''
	while IPPORT==IPPORTref:
		IPPORT=getGameServer.getServerIp()
		if IPPORT == ["false",0000]:
			exit()



	sys.stdout.write("Server found at {} \n".format(IPPORT))
	sys.stdout.flush()
	QUERYIPPORT=None
	retryTime=60
	while QUERYIPPORT==None:
		
		QUERYIPPORT=getIpPort.getIpPort(IPPORT)
		if QUERYIPPORT==None:
			print_at(3,0,"failed to get query-port... retrying in {} seconds".format(str(retryTime)))
			for sec in range(1,retryTime):
				time.sleep(1)
				print_at(3,28,"retrying in {} seconds ".format(retryTime-sec))
	print("Queryport {} found... beginning scans".format(QUERYIPPORT[1]))
	
	i=0
	while True:
		if QUERYIPPORT!=None:
			with open('./config/config.json') as json_file:
				config = json.load(json_file)
			
			i+=1
			info=getInfo.GetInfo(QUERYIPPORT)
			try:
				label.config(fg=config["config"]["TextColour"])
				print_at(6,0,"Players: {}/{} \nTime:	{}\n {}".format(info["Players"], info["MaxPlayers"], (info["Tags"].split(","))[-1], i))
				label.config(text="Players: {}/{} \n  Time:	 {}".format(info["Players"], info["MaxPlayers"], (info["Tags"].split(","))[-1]))
				
			except:
				print_at(6,0,"Error...")
				label.config(fg="red")
				
		else:
			print("query port not found")
		time.sleep(config["config"]["updateRate"])
def refStarter(label):
	t=threading.Thread(target=refreshStats, args=(label,))
	t.start()

label = tkinter.Label(text='Loading...', font=('verdana ','16'), fg=config["config"]["TextColour"], bg=config["config"]["BGColour"])
label.master.overrideredirect(True)
with open('./config/config.json') as json_file:
				config = json.load(json_file)
label.master.geometry("+"+config["config"]["PfromSide"]+"+"+config["config"]["PfromTop"])
label.master.lift()
label.master.wm_attributes("-topmost", True)
label.master.wm_attributes("-disabled", True)
label.master.wm_attributes("-transparentcolor", config["config"]["BGColour"])
label.after(1 ,refStarter(label))
hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
t = threading.Thread(target=watchdogLocal.start, args=(label,))
t.start()
t2 = threading.Thread(target=keybindsLocal.start, args=(label,))
t2.start()

label.pack()
label.mainloop()
