import RPi.GPIO as GPIO
import time
import os

class RaspiBoard():

	LED=19
	IN1=21
#    IN2=22
#    IN3=4

	def __init__(self):
		'''
		Constructor        '''
		GPIO.cleanup()
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.LED, GPIO.OUT)
		GPIO.output(self.LED,True)
		GPIO.setup(self.IN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#        GPIO.setup(self.IN2, GPIO.IN)
#        GPIO.setup(self.IN3, GPIO.IN)

	def destroy(self):
		GPIO.cleanup()
	
	def keyPressed(self):
		if(GPIO.input(self.IN1) == True): return 1
 #       if(GPIO.input(self.IN2) == True): return 2
 #       if(GPIO.input(self.IN3) == True): return 3
		return 0