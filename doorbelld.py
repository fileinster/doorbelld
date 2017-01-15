#!/usr/bin/env python2.7  
# Button action script by Phil Leinster
# Orignal inspiration based on http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3  
# V1.0 29.05.2016
# V1.2 20/11.2016 - Updated for implementation.
import RPi.GPIO as GPIO, time, subprocess, threading, socket, signal
from settings import BUTTON,LED,HOSTS,PORT
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class GracefulKiller:
	kill_now = False
	def __init__(self):
		signal.signal(signal.SIGINT, self.exit_gracefully)
		signal.signal(signal.SIGTERM, self.exit_gracefully)

	def exit_gracefully(self,signum, frame):
		print "Recieved " + SIGNNAME[signum] + "."
		self.kill_now = True
		GPIO.cleanup()
		print "Stopping doorbell service."
		raise SystemExit

SIGNNAME = dict((getattr(signal, n), n) \
for n in dir(signal) if n.startswith('SIG') and '_' not in n )

# GPIO button set up as input, pulLED up to avoid false detection.  
# It is wired to connect to GND on button press.  
# So setting up falling edge detection for both  
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED,True)

def chime():
	print ("Sending command to chimer.")
	for host in HOSTS:
		print "Connect to host: " + str(host)
	        s = socket.socket()
		s.connect((host,PORT))
		s.send("chime\n")
		s.close

def notify():
	subprocess.call(["notify", "-t", "\"Ding Dong!\""])

# now we'll define a threaded callback functiona 
# it will run in another thread when our events are detected
def buttonpressed(channel):  
	if GPIO.input(BUTTON):
		GPIO.output(LED,True)
		print "rising edge detected on " + str(BUTTON)
	else:
		GPIO.output(LED,False)
		t1 = threading.Thread(target=chime)
		#t2 = threading.Thread(target=notify)
		t1.start()
		#t2.start()
		print "falling edge detected on " + str(BUTTON)
		t1.join()
		#t2.join()

# when a falling edge is detected on button, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
GPIO.add_event_detect(BUTTON, GPIO.BOTH, callback=buttonpressed, bouncetime=100)  
print "Waiting for doorbell to ring"  

killer = GracefulKiller()
while True:
	try:  
		time.sleep(3600)
		print "still waiting for doorbell..."
 
	except KeyboardInterrupt:  
		GPIO.cleanup()       # clean up GPIO on CTRL+C exit
		print "Exption caught after timer."
		if killer.kill_now:
			break

GPIO.cleanup()           # clean up GPIO on normal exit  


