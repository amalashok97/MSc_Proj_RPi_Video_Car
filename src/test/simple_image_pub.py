#!/usr/bin/python
# Initial QR-detecting script.
# !!! Does not use the default python zbar !!!
# Instead it uses https://github.com/zplab/zbar-py, since this wrapper also
# allows for code location to be returned

import cv2
import sys
import numpy as np
import Image

from qr_tracker.msg import Movements, Text_image, Help, Image_Text, Qr_code
import StringIO
import time
import rospy
import zbar
import socket
import message_filters
from cv_bridge import CvBridge, CvBridgeError
from virtual_battery import VirtualBattery
import psutil
import os
import pytesseract

from subprocess import check_output
print check_output(['hostname','-I'])
wlan_ip = check_output(['hostname','-I'])


cache=None
DISCHARGE_INTERVAL = 10
battery = VirtualBattery(discharge_interval=DISCHARGE_INTERVAL)
pub = None
cap = None
rate = None
help_top=None
qr_code="ROSberry Pi"
looked_left=False
finalIp=wlan_ip

forwards_threshold = 180
backwards_threshold = 280
pan_threshold = 80
tilt_threshold = 60
frame_skip = 5
Current_x=0
Current_y=0
def current_position():
        global Current_y, Current_x
        return (Current_x, Current_y)
		

def callback(data):
        
        if data.found =='n':
                global qr_code,finalIp 
                qr_code = data.qr
		finalIp = data.ip
        else:
                cap.release()

                
        
        rospy.loginfo("The Qr code we are looking for is ",data.qr)



def choose(data):
        #check if the chooden robot is this one
        chooseip = data.choosenip
	global looked_left
        if chooseip==wlan_ip:
		bridge = CvBridge()
		#if it is take the ros image and tranform to cv2 image
		try:
                	img= bridge.imgmsg_to_cv2(data.im, desired_encoding="passthrough")
			if not looked_left:
				cv2.imwrite('temp.jpg',img)
				looked_left=True 
#check for text in image
				text = pytesseract.image_to_string(Image.open('temp.jpg'))
			#publish final text and origional ip
				ret = rospy.Publisher("return_text", Image_Text, queue_size=5)
				ret.publish(finalIp, text)
		except CvBridgeError as e:
			print(e)

def finalReturn(data):
        #print the text from the image
	if data.finalip==socket.gethostbyname(socket.gethostname()):
		print(data.text)   	

def task_dist(img):

	msg = Text_image(wlan_ip,wlan_ip,img)
        rob=rospy.Publisher("pic",Text_image, queue_size=10)
        rob.publish(msg)        


def main():
	
	global pub, rate,text,qr,help,battery,Current_x,Current_y,wlan_ip
	battery.start_drain()
	#camera and movement
	rospy.init_node("camera_stream", disable_signals=True)


	
	#qr code input sets global qr_code via callback
	
	
	qr = rospy.Subscriber("qr_message", Qr_code, callback)
        
	
	#get picture
	choosen = rospy.Subscriber("pic",Text_image, choose)

	#get return text
	text = rospy.Subscriber("return_text", Image_Text, finalReturn)
                              
	try:
		global cap, pub, rate,text,qr_code,looked_left
		cap = cv2.VideoCapture(0)
		i = 0 
		while not rospy.is_shutdown():


			# Capture frame-by-frame
			try:
				ret, frame = cap.read()
				image = cv2.cvtColor( frame, cv2.COLOR_RGB2GRAY )
				scanner = zbar.Scanner()
				#scanner.parse_config('enable')
				
				results = scanner.scan(image)
				cv2.imwrite('fromcam.jpg',image)

				for result in results:
					#print "Processing results: ",len(results)
					#print(result.type, result.data, result.quality, result.position)
					
					if qr_code is not None and (qr_code==result.data):
						br = CvBridge()
                                       		img = br.cv2_to_imgmsg(image, encoding="passthrough")
						if looked_left:
							task_dist(img)
 	

				
			except KeyboardInterrupt:
				break
	
	except KeyboardInterrupt:
		print("Terminating program...")
		cap.release()
		server.socket.close()


if __name__ == '__main__':
	main()
