import RPi.GPIO as GPIO
import time
import random

servo_port_1 = 11
servo_port_2 = 13

servo_1_min_duty = 2.5
servo_1_max_duty = 10
servo_2_min_duty = 2.5
servo_2_max_duty = 11

def initialize_servos():
	global servo_port_1, servo_port_2
	global servo1, servo2

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(servo_port_1, GPIO.OUT)
	GPIO.setup(servo_port_2, GPIO.OUT)

	servo1 = GPIO.PWM(servo_port_1, 50)
	servo2 = GPIO.PWM(servo_port_2, 50)

	return (servo1, servo2)

def cleanup():
	GPIO.cleanup()

#from a 180-ish range of motion, where 0 is the middle
def move_angle(servo, angle):
	actual_angle = angle + 90
	
	#TODO fix this later, right now thos are magic numbers (s1 max - min), s1 min
	duty = (actual_angle/180) * 8 + 2.5
	servo.ChangeDutyCycle(duty)

def dance(servo):	
	for i in range(1000):
		angle = random.randint(0,180)
		move_angle(servo, angle)
		time.sleep(1)

