
import RPi.GPIO as GPIO
import time
from gpiozero import LED, Button
led1=Button(21)
for i in range(200):
	print("a")
	led1.on()
	time.sleep(.20)
	print("b")
	led1.off()
	time.sleep(.20)

