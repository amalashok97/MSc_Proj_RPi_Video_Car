#!/usr/bin/python
import motor
import motor_direction
import camera_direction
import rospy
import time
import numpy as np
from qr_tracker.msg import Movements

from subprocess import check_output
print check_output(['hostname','-I'])
wlan_ip = check_output(['hostname','-I'])

delay_interval = 0.3
motor_runtime = 0.3

def map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def code_refocus(msg):
	move_direction = msg.motor_direction
	pan_degree = msg.pan_degree
	tilt_degree = msg.tilt_degree

	if move_direction != 's' and msg.wlan_ip == wlan_ip :
		print "Code too far or too close."
		if pan_degree:
			motor_direction.home()
			#motor_direction.calibrate(64)
			print "Cam-Motor: Code also not centered. Panning..."
			move_camera("pan", pan_degree)
			
			print "Cam-Motor: Turning wheels..."
			turn_wheels(pan_degree)
			print "Cam-Motor: Moving..."
			move_wheels(move_direction)
			print "Cam-Motor: Returning home..."
			motor_direction.home()
			#motor_direction.calibrate(64)
		else:
			print "Motor: Moving..."
			motor_direction.home()
			move_wheels(move_direction)
			camera_direction.home()

		if tilt_degree:
			print "Cam-Motor: Code also not centered. Tilting..."
			move_camera("tilt", tilt_degree)
			
	elif msg.wlan_ip==wlan_ip:
		if pan_degree:
#			print "Panning..."
			move_camera("pan", pan_degree)
		if tilt_degree:
			print "Tilting..."
			move_camera("tilt", tilt_degree)

def turn_wheels(angle):
	#print "Raw angle: ", angle
	angle = map(angle, -320, 320, 0, 255)
	print 
	print "Turning wheels at angle: ", angle
	time.sleep(delay_interval)
	motor_direction.turn(255-angle)
	time.sleep(delay_interval)
	#motor_direction.turn_right()

def move_wheels(direction):
	#print direction
	time.sleep(delay_interval)
	motor.motor_control(direction)
	time.sleep(motor_runtime)
	motor.stop()

def move_camera(movement, step):
	time.sleep(delay_interval)
#	print "Camera's current position: ", camera_direction.current_position()
#	print "Raw step: ", step
	#step = map(step, -320, 320, 0, 255)
	if movement=="pan":
		#camera_direction.pan(15*np.sign(step))
		camera_direction.pan(step/12)
	if movement=="tilt":
		#camera_direction.tilt(-15*np.sign(step))			
		camera_direction.tilt(step/12)
	time.sleep(delay_interval)


def main():
	motor.setup()
	motor_direction.setup()
	#motor_direction.home()
	camera_direction.setup()
	camera_direction.home()
	
	rospy.init_node("robot_movement")
	rospy.Subscriber('move_instructions', Movements, code_refocus)
	rospy.spin()


if __name__ == '__main__':
	main()
