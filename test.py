
import RPi.GPIO as GPIO
import time
from gpiozero import LED, Button
step=LED(2)
for _ in range(200):
	print('a')
	step.on()
	time.sleep(.01)
	step.off()
	
