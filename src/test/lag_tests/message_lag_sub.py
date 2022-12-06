#!/usr/bin/python
import rospy
import time
from qr_tracker.msg import TestString
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
bridge = CvBridge()
filetext = open("test_string.txt","a")
filetextimage = open("test_image.txt","a")

timels = []
image_time = []
def tally_time(data):
	
	timestamp = str(data.h.stamp.secs)+'.'+str(data.h.stamp.nsecs)
	
	t= rospy.Time.now()
	timestamp2 = str(t.secs) + "." +str(t.nsecs)

	filetext.write(str(float(timestamp2)-float(timestamp)))
	filetext.write("\n")

def tally_time_image(data):
	try:
#cv_img = bridge.imgmsg_to_cv2(data.data,data.enconding)
		timestamp = str(data.h.stamp.secs)+'.'+str(data.h.stamp.nsecs)
	
		t= rospy.Time.now()
		timestamp2 = str(t.secs) + "." +str(t.nsecs)

		filetext.write(str(float(timestamp2)-float(timestamp)))
		filetext.write("\n")



	except CvBridgeError,e:
		print(e)

def main():
	rospy.init_node('simple_listener_2')
	string = rospy.Subscriber("basic",TestString,tally_time)
	image = rospy.Subscriber("image",Image, tally_time_image,buff_size=2**24)
	rospy.spin()


if __name__ == '__main__':
        main()

