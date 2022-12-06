#!/usr/bin/python
# Initial QR-detecting script.
# !!! Does not use the default python zbar !!!
# Instead it uses https://github.com/zplab/zbar-py, since this wrapper also
# allows for code location to be returned

import cv2
import sys
import numpy as np
import Image
from std_msgs.msg import Header
from qr_tracker.msg import Movements, Text_image, Help, Image_Text, Qr_code
import rospy
import message_filters
from cv_bridge import CvBridge, CvBridgeError
import os
import pytesseract
import psutil
sent=False

from subprocess import check_output
wlan_ip = check_output(['hostname','-I'])
cache=None
looked_left=False

def helpmessage(data):
	global battery
        # get info on robot cpu memory and battery
	#publish help message with ip, battery,cpu mem and ip again
	help_top = rospy.Publisher("help_ret", Help,queue_size=100)
	rospy.sleep(1)

	h = Header()
	h.stamp = rospy.Time.now()
    cpu_percent =100- psutil.cpu_percent(interval=None, percpu=False)
	process = psutil.Process(os.getpid())
	mem = str(process.memory_percent())
    bat=str(battery.battery_percentage())
#        publish along with ip of robot to return it to and this ip
	help_top.publish(h,data.returnip,str(cpu_percent),bat,mem, wlan_ip)

def choose(data):
        #check if the chooden robot is this one
	global wlan_ip
	if data.choosenip==wlan_ip:
		bridge = CvBridge()
		#if it is take the ros image and tranform to cv2 image
		try:
			img= bridge.imgmsg_to_cv2(data.im, desired_encoding="passthrough")
			print "finding text"

			cv2.imwrite('temp.jpg',img)
			#check for text in image
			img = Image.fromarray(img)
			text = pytesseract.image_to_string(img)
			#publish final text and origional ip
			ret = rospy.Publisher("return_text", Image_Text, queue_size=5)
			rospy.sleep(1)
			ret.publish(data.returnip, text)
			print text

		except CvBridgeError as e:
			print(e)

def finalReturn(data):
        #print the text from the image
	if data.finalip==wlan_ip:
		print(data.text)

def main():
	rospy.init_node("floating_pi", disable_signals=True)
	#get picture
	choosen = rospy.Subscriber("pic",Text_image, choose)

	help_msg = rospy.Subscriber("help",Help,helpmessage)
	#get return text
	text = rospy.Subscriber("return_text", Image_Text, finalReturn)
	try:
		while not rospy.is_shutdown():
			rospy.spin()
	except KeyboardInterrupt:
                print("Terminating program...")


if __name__ == '__main__':
	main()
