import RPi.GPIO as GPIO

servo_port_1 = 11
servo_port_2 = 13

servo_1_min_duty = 2.5
servo_1_max_duty = 10
servo_2_min_duty = None
servo_2_max_duty = None

def initialize_servos():
	global servo_port_1, servo_port_2
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(servo_port_1, GPIO.OUT)
	GPIO.setup(servo_port_2, GPIO.OUT)

def cleanup():
	pass

