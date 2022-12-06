#!/usr/bin/python
import rospy
import time
import os
import psutil

import cv2
import numpy as np
import Image
import pytesseract

from qr_tracker.msg import Image_Text,Text_image
from std_msgs.msg import Header
from cv_bridge import CvBridge, CvBridgeError
from virtual_battery import VirtualBattery
DISCHARGE_INTERVAL = 10
battery = VirtualBattery(discharge_interval=DISCHARGE_INTERVAL)

#setting this ip
from subprocess import check_output
print check_output(['hostname','-I'])
wlan_ip = check_output(['hostname','-I'])


filetext = open("process_image.txt","a")

def choose(data):
        #check if the chooden robot is this one
 	global wlan_ip
	if not data.chooseip==wlan_ip:
		bridge = CvBridge()
		#if it is take the ros image and tranform to cv2 image
		try:
                	img= bridge.imgmsg_to_cv2(data.im, desired_encoding="passthrough")
			#print "finding text"
			cv2.imwrite('temp.jpg',img)
                        #check for text in image
			text = pytesseract.image_to_string(Image.open('temp.jpg'))
			#publish final text and origional ip
			ret = rospy.Publisher("return_text", Image_Text, queue_size=5)
			rospy.sleep(1)
			filetext.write("text " + text)
			ret.publish(finalIp, text)
			


		except CvBridgeError as e:
			print(e)


def main():

	#get picture
	choosen = rospy.Subscriber("pic",Text_image, choose)
	rospy.init_node('img_lag_sub_1')
	r=rospy.Rate(10)
	battery.start_drain()
	br = CvBridge()

	while not rospy.is_shutdown():
		rospy.spin()


if __name__ == '__main__':
        main()
