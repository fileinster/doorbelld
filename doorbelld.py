#!/usr/bin/env python2.7  
# Button action script by Phil Leinster
# Orignal inspiration based on http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3  
# V1.0 29.05.2016
# V1.2 20/11.2016 - Updated for implementation.
import RPi.GPIO as GPIO, time, subprocess, threading, socket, signal
from sipclient import doorbell

GPIO.cleanup()           # clean up GPIO on normal exit  
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

SIGNNAME = dict((getattr(signal, n), n) \
for n in dir(signal) if n.startswith('SIG') and '_' not in n )

button=21
led=19


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

def chime():
	global queue 
	print ("Sending command to chimer.")
	s = socket.socket()
	host = 'chimer1.local'
	port = 5000
	s.connect((host,port))
	s.send('chimer\n')
	s.close
	queue = queue - 1
	#subprocess.call(["ssh", "phil@192.168.1.159", "sudo aplay doorbell.wav"])

def notify():
	subprocess.call(["notify", "-t", "\"Ding Dong!\""])

# now we'll define a threaded callback functiona 
# it will run in another thread when our events are detected
def buttonpressed(channel):  
	global queue 
	if GPIO.input(led):
		GPIO.output(led,True)
		print "rising edge detected on " + button
	else:
		if queue < 1:
			GPIO.output(led,False)
			t1 = threading.Thread(target=chime)
			#t2 = threading.Thread(target=notify)
			queue = queue + 1
			t1.start()
			t2.start()
		print "falling edge detected on " + button

def log(msg):
    print "[",datetime.datetime.now(), "] ", msg






# GPIO button set up as input, pulled up to avoid false detection.  
# It is wired to connect to GND on button press.  
# So setting up falling edge detection for both  
#GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
#GPIO.setup(led, GPIO.OUT)
#GPIO.output(led,True)

# when a falling edge is detected on button, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
#GPIO.add_event_detect(button, GPIO.BOTH, callback=buttonpressed, bouncetime=20)  
print "Waiting for doorbell to ring"  
queue = 0






killer = GracefulKiller()
db = doorbell()
db.run()
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

