#!/usr/bin/python
import rospy
import time
from std_msgs.msg import Float64
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
bridge = CvBridge()
filetext = open("test_string.txt","a")
filetextimage = open("test_image.txt","a")

timels = []
image_time = []
def tally_time(data):
	now=time.time()
	timels.append([data,now])	
	filetext.write(str(data.data-now))
	filetext.write("\n")

def tally_time_image(data):
	now=str(rospy.Time.now())
	try:
		#cv2_img = bridge.imgmsg_to_cv2(data.data,data.enconding)
		timels.append([float(now), float(str(data.header.stamp.secs)+'.'+str(data.header.stamp.nsecs))])	
		filetextimage.write(str(float(str(data.header.stamp.secs)+'.'+str(data.header.stamp.nsecs))-float(now)))
		filetextimage.write("\n")
	except CvBridgeError,e:
		print(e)

def main():
	rospy.init_node('simple_listener')
	string = rospy.Subscriber("basic",Float64,tally_time)
	image = rospy.Subscriber("image",Image, tally_time_image)
	rospy.spin()	


if __name__ == '__main__':
        main()

