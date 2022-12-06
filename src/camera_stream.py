#!/usr/bin/python
# Initial QR-detecting script.
# !!! Does not use the default python zbar !!!
# Instead it uses https://github.com/zplab/zbar-py, since this wrapper also
# allows for code location to be returned

import cv2
import sys
import os
import psutil

import numpy as np
import Image
import pytesseract

from std_msgs.msg import Header
from qr_tracker.msg import Movements, Text_image, Help, Image_Text, Qr_code

import StringIO
import time
import rospy
import zbar
import socket

import message_filters as mf
from cv_bridge import CvBridge, CvBridgeError
from virtual_battery import VirtualBattery

#start virtual battery
DISCHARGE_INTERVAL = 10
battery = VirtualBattery(discharge_interval=DISCHARGE_INTERVAL)

pub = None
cap = None
help_top=None
qr_code=None
looked_left=False
finalIp=None
found = True

cache_messages=[]

#setting this ip
from subprocess import check_output
#print check_output(['hostname','-I'])
wlan_ip = check_output(['hostname','-I'])

def mycallback(data):
	print "\n"

#movement parameters
forwards_threshold = 180
backwards_threshold = 280
pan_threshold = 80
tilt_threshold = 60
frame_skip = 5
startx=100

Current_x=0
Current_y=0


def current_position():
        global Current_y, Current_x
        return (Current_x, Current_y)


def callback(data):
		#qr_message topic 
        global found,qr_code,finalIp 
        if data.found =='n':           
                qr_code = data.qr
		finalIp = data.ip
		found=False
        else:
                qr_code=None
		found=True
	print(data.qr) 

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

def task_dist(image):
        #publish found message
	global battery
	print "starting task dist"
        found_qr = rospy.Publisher("qr_message", Qr_code, queue_size=100)
        rospy.sleep(1)
	found_qr.publish(finalIp,qr_code,'y')
	
        #publish help message with ip, battery,cpu mem and ip again
	help_top = rospy.Publisher("help", Help,queue_size=100)
	rospy.sleep(1)

	h = Header()
	h.stamp = rospy.Time.now()
	cpu_percent =100- psutil.cpu_percent(interval=None, percpu=False)
	process = psutil.Process(os.getpid())
	mem = str(process.memory_percent())
        bat=str(battery.battery_percentage())
#        publish along with ip of robot to return it to and this ip
        help_top.publish(h,wlan_ip,str(cpu_percent),bat,mem, wlan_ip)
	timems = rospy.Time.now()
	#print(finalIp,qr_code, found)
	return timems


def main():

	global cap,pub,rate,help,battery,Current_x,Current_y
	battery.start_drain()
	#camera and movement
	rospy.init_node(("camera_stream2"), disable_signals=True)
	pub = rospy.Publisher('move_instructions',Movements , queue_size=10)
	rate = rospy.Rate(10)


	#qr code input sets global qr_code via callback
	qr = rospy.Subscriber("qr_message", Qr_code, callback)

	#get help message
	help = rospy.Subscriber("help", Help, helpmessage)

	#get picture
	choosen = rospy.Subscriber("pic",Text_image, choose)

	#get return text
	text = rospy.Subscriber("return_text", Image_Text, finalReturn)
	scanner = zbar.Scanner()
	try:
		global found, qr_code, looked_left, wlan_ip, cache_messages, finalIp, cache
		cap = cv2.VideoCapture(0)
		i = 0 
		while not rospy.is_shutdown():

			# Capture frame-by-frame
			try:
				ret, frame = cap.read()
				grey = cv2.cvtColor( frame, cv2.COLOR_RGB2GRAY )
				image=grey
				#thresh = cv2.threshold(grey,0,255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
				#image = cv2.medianBlur(grey,3)
#				cv2.rectangle(frame, (220, 140), (420, 340), (255, 0, 0), 2)
				results = scanner.scan(grey)
				time.sleep(3)
				if results==[] and found==False:
				        if  looked_left and (Current_x<(80)):
						camera_x =(2*60)
                                      		Current_x+=10
					elif (current_position()[0] >=(80)):
						camera_x=(2*60)
                                               	looked_left = False

					if not looked_left and (Current_x>(-80)):
						camera_x = -(2*60)
						Current_x+= (-10)
					elif (current_position()[0] <=(-80)):
						camera_x=-(2*60)
						looked_left=True

                                        camera_y = current_position()[1]
					Current_y=0
                                        move_direction = 's'
                                        pan_degree = camera_x
                                        tilt_degree = camera_y

                                        pub.publish(wlan_ip,move_direction, pan_degree, tilt_degree)


				for result in results:
					print results
					if len(result.position)!=4:
						break;


					if qr_code is not None and (qr_code==result.data) and found==False:
						print "found qr_code"

						br = CvBridge()
						found=True

                                       		img = br.cv2_to_imgmsg(image, encoding="passthrough")
						sub=mf.Subscriber("help_ret",Help)
						cache = mf.Cache(sub,cache_size=10)
						cache.registerCallback(mycallback)

						start_time=task_dist(img)
						time.sleep(3)
						cachemes = cache.getInterval(start_time, rospy.Time.now())

					#get the best robot for the job
						minim=float("inf")

						robo=None
						curr_time = rospy.Time.now()
						for message in cachemes:
							print message
							time_f=rospy.Time((message.header.stamp.secs),(message.header.stamp.nsecs))
							resources = (2*float(message.cpu))*float(message.memory)*(2*(100 - float(message.battery)))*(curr_time-time_f).to_sec()
							if resources<minim:
								minim=resources
								robo=message
					#publish the picture to that robot				

						rob=rospy.Publisher("pic",Text_image, queue_size=10)
						rospy.sleep(1)
						if finalIp is None:
							finalIp= wlan_ip
	
						
						if robo is None:
							rob.publish(finalIp,wlan_ip,img)
						else:
							rob.publish(finalIp,robo.ip,img)



####
				#	if i%frame_skip==0:
				#		code_size = result.position[1][1]-result.position[0][1]
				#		cv2.rectangle(image, result.position[0], result.position[2], (255, 255, 255), 2)
				#		renderpt = ((result.position[1][0]+result.position[2][0])/2+code_size/4, (result.position[1][1]+result.position[2][1])/2+code_size/4)
				#		cv2.putText(image, result.data, org=renderpt, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.9, color=(255, 255, 255), thickness=3)

#						move_direction = 'f' if code_size<forwards_threshold else ('b' if code_size>backwards_threshold else 's')
						#print "Not optimal distance from code."

				#		frame_centre_x = image.shape[1]/2
				#		frame_centre_y = image.shape[0]/2
				#		code_centre_x = (result.position[0][0]+result.position[2][0])/2
				#		code_centre_y = (result.position[0][1]+result.position[2][1])/2
				#		correction_x = frame_centre_x - code_centre_x
				#		correction_y = frame_centre_y - code_centre_y

				#		pan_degree = correction_x if abs(correction_x)>pan_threshold else 0
				#		tilt_degree = correction_y if abs(correction_y)>tilt_threshold else 0

#						pub.publish(wlan_ip, move_direction, pan_degree, tilt_degree)
####
						rate.sleep()
				i += 1


			except KeyboardInterrupt:
				break

	except KeyboardInterrupt:
		print("Terminating program...")
		cap.release()



if __name__ == '__main__':
	main()
