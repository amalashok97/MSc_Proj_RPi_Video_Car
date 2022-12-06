#!/usr/bin/env python
import Sunfounder_PWM_Servo_Driver.Servo_init as servo
#import time                # Import necessary modules

leftPWM = 400
rightPWM = 500
homePWM = 450

def Map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setup():
	global leftPWM, rightPWM, homePWM, pwm
	#leftPWM = 400
	#homePWM = 450
	#rightPWM = 500
	offset =0
	try:
		for line in open('/home/pi/ros_catkin_ws/src/qr_tracker/src/config','r'):
			if line[0:8] == 'offset =':
				offset = int(line[9:-1])
		print "wheel turn offset: ",offset
	except:
		print 'config error'
	leftPWM += offset
	homePWM += offset
	rightPWM += offset
	print "Motor offset left: ", leftPWM
	print "Motor offset right: ", rightPWM
	pwm = servo.init()         # Initialize the servo controller.

# ==========================================================================================
# Control the servo connected to channel 0 of the servo control board, so as to make the 
# car turn left.
# ==========================================================================================
def turn_left():
	#print "Turning left."
	global leftPWM
	pwm.setPWM(0, 0, leftPWM)  # CH0

# ==========================================================================================
# Make the car turn right.
# ==========================================================================================
def turn_right():
	#print "Turning right."
	global rightPWM
	pwm.setPWM(0, 0, rightPWM)

# ==========================================================================================
# Make the car turn back.
# ==========================================================================================

def turn(angle):
	global leftPWM, rightPWM
	angle = Map(angle, 0, 255, leftPWM, rightPWM)
	print "MOTOR: Actual turning angle: ", angle
	print "MOTOR: Actual PWM: ", leftPWM, rightPWM
	pwm.setPWM(0, 0, angle)

def home():
	global homePWM
	pwm.setPWM(0, 0, homePWM)

def calibrate(x):
	pwm.setPWM(0, 0, 450+x)

# def test():
# 	while True:
# 		turn_left()
# 		time.sleep(1)
# 		home()
# 		time.sleep(1)
# 		turn_right()
# 		time.sleep(1)
# 		home()

# if __name__ == '__main__':
# 	setup()
# 	home()


