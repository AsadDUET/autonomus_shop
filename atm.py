
from time import sleep
import random
import RPi.GPIO as GPIO
from gpiozero import LED, Button
import easydriver as ed
#~ import label_image
servo=LED(4)
#top_light=LED(3)
#bottom_light=LED(2)
ir=Button(16)
#pir=Button(9)


servo.off()
#top_light.off()
#bottom_light.off()

taka = ed.easydriver(2, 0.0004, 22)
chips_motor=ed.easydriver(19, 0.004)
chocolate_motor=ed.easydriver(14, 0.004)
drawer=ed.easydriver(21, 0.0004,20)
def supply():
	drawer.set_direction(True) # True = close
	for i in range(4300):
		drawer.step()
	sleep(3)
	drawer.set_direction(False) # True = close
	for i in range(4300):
		drawer.step()
def give_chips(num):
	for i in range(num*1600):
		chips_motor.step()
def give_chocolate(num):
	for i in range(num*1600):
		chocolate_motor.step()
def take_taka():
	sleep(5)
	taka.set_direction(True)
	servo.on()
	for i in range(0,4000):
		taka.step()
	servo.off()
def back_taka():
	servo.on()
	taka.set_direction(False)
	for i in range(0,4000):
		taka.step()
	servo.off()
def reset():
	taka.set_direction(False)
	for i in range(0,4000):
		taka.step()
def start_atm():
	ir.wait_for_press()
	sleep(4)
	take_taka()
	back_taka()
if __name__=="__main__":
	while True:
		start_atm()
		give_chips(1)
		give_chocolate(1)
		supply()
		print('aa')
