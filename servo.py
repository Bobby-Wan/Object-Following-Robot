import RPi.GPIO as GPIO
import time
import random

class ServoConfig:
	def __init__(self, min_duty, max_duty, pin):
		self.min_duty = min_duty
		self.max_duty = max_duty
		self.pin = pin
		self.duty_range = max_duty - min_duty
		self.duty = min_duty + (self.duty_range)/2
		self.angle = duty_to_angle(self.duty, self.duty_range, min_duty, 180)

pan_servo_pin = 13
pan_servo_min_duty = 2.5
pan_servo_max_duty = 11

tilt_servo_pin = 11
tilt_servo_min_duty = 2.5
tilt_servo_max_duty = 10

pan_config = ServoConfig(pin=pan_servo_pin, min_duty=pan_servo_min_duty, max_duty=pan_servo_max_duty)
tilt_config = ServoConfig(pin=tilt_servo_pin, min_duty=tilt_servo_min_duty, max_duty=tilt_servo_max_duty)

def angle_to_duty(angle, angle_range, duty_range, duty_min):
	return angle/float(angle_range) * duty_range + duty_min

def duty_to_angle(duty, duty_range, duty_min, angle_range):
	return ((duty - duty_min)/duty_range) * angle_range

def initialize_servos():
	# global pan_servo_pin, tilt_servo_pin

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pan_config.pin, GPIO.OUT)
	GPIO.setup(tilt_config.pin, GPIO.OUT)

	pan_servo = GPIO.PWM(pan_config.pin, 50)
	tilt_servo = GPIO.PWM(tilt_config.pin, 50)

	pan_servo.start(pan_config.duty)
	tilt_servo.start(tilt_config.duty)

	return (pan_servo, tilt_servo)

def cleanup():
	GPIO.cleanup()

#from a 180-ish range of motion, where 0 is the middle
def move(servo, servo_config, angle):
	range_of_motion = servo_config.max_duty - servo_config.min_duty

	#calculate the actual duty needed for that angle
	duty = angle_to_duty(angle, 180, servo_config.duty_range, servo_config.min_duty)
	servo.ChangeDutyCycle(duty)

#test function
def dance(servo, servo_config):	
	for i in range(1000):
		angle = random.randint(0,180)
		move(servo, servo_config, angle)
		time.sleep(1)