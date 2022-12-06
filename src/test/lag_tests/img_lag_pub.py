#!/usr/bin/python
import rospy
import time
import os
import psutil

import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import Image
import pytesseract

from qr_tracker.msg import Image_Text,Text_image
from std_msgs.msg import Header

from virtual_battery import VirtualBattery
DISCHARGE_INTERVAL = 10
battery = VirtualBattery(discharge_interval=DISCHARGE_INTERVAL)
filetext = open("text_return.txt","a")

#setting this ip
from subprocess import check_output
print check_output(['hostname','-I'])
wlan_ip = check_output(['hostname','-I'])

finished=True,
starttime = 0

def finalReturn(data):
	global finished
        #print the text from the image
	now = rospy.Time.now()
	filetext.write(str(starttime - now))
	filetext.write("/n")
	finished=True

def main():
	global finished, starttime
	#get return text
	text = rospy.Subscriber("return_text", Image_Text, finalReturn)
	
	pic = rospy.Publisher("pic",Text_image,queue_size=100)
	rospy.init_node('img_lag_pub')
	r=rospy.Rate(10)
	battery.start_drain()
	br = CvBridge()
	n=0
	try:
		while not rospy.is_shutdown() and n<300:
			if finished==True:
				print "m"
				h = Header()
				h.stamp = rospy.Time.now()
				starttime = rospy.Time.now()
				image = cv2.imread('jpeg.jpg',0)
				img = br.cv2_to_imgmsg(image, encoding="passthrough")

				pic.publish(wlan_ip,wlan_ip,img)
				finished=False
	except KeyboardInterrupt:
		print("terminating")

if __name__ == '__main__':
        main()

