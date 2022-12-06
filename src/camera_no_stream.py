#!/usr/bin/python
# Initial QR-detecting script.
# !!! Does not use the default python zbar !!!
# Instead it uses https://github.com/zplab/zbar-py, since this wrapper also
# allows for code location to be returned

import cv2
import sys
import numpy as np
import Image
from qr_tracker.msg import Movements
import time
import rospy
import zbar

pub = None
cap = None
rate = None
pan_threshold = 150
tilt_threshold = 150
		
	
def QR_tracker(device_ID):
	global cap, pub, rate
	cap = cv2.VideoCapture(device_ID)

	while not rospy.is_shutdown():
		# Capture frame-by-frame
		try:
			ret, frame = cap.read()
			image = cv2.cvtColor( frame, cv2.COLOR_RGB2GRAY )
			cv2.rectangle(frame, (220, 140), (420, 340), (255, 0, 0), 2)

			scanner = zbar.Scanner()
			results = scanner.scan(image)

			for result in results:
				#print "Processing results: ",len(results)
				#print(result.type, result.data, result.quality, result.position)
				cv2.rectangle(image, result.position[0], result.position[2], (255, 255, 255), 2)
				renderpt = ((result.position[1][0]+result.position[2][0])/2+90, (result.position[1][1]+result.position[2][1])/2)
				cv2.putText(image, result.data, renderpt, cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
				code_size = result.position[1][1]-result.position[0][1]

				
				move_direction = 'f' if code_size<100 else ('b' if code_size>300 else 's')
					#print "Not optimal distance from code."

				frame_centre_x = image.shape[1]/2
				frame_centre_y = image.shape[0]/2
				code_centre_x = (result.position[0][0]+result.position[2][0])/2
				code_centre_y = (result.position[0][1]+result.position[2][1])/2
				correction_x = frame_centre_x - code_centre_x
				correction_y = frame_centre_y - code_centre_y

				pan_degree = correction_x if abs(correction_x)>pan_threshold else 0
				tilt_degree = correction_y if abs(correction_y)>tilt_threshold else 0

				pub.publish(move_direction, pan_degree, tilt_degree)
				rate.sleep()
		except:
			print "Error reading from camera!"



def main():
	global pub, rate

	rospy.init_node("camera_no_stream")
	pub = rospy.Publisher('move_instructions', Movements , queue_size=10)
	rate = rospy.Rate(10)
	QR_tracker(0)


if __name__ == '__main__':
	main()
