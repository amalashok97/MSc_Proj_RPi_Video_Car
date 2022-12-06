#!/usr/bin/python
import rospy
import time
from std_msgs.msg import Header
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
br = CvBridge()


def main():
#	cap = cv2.VideoCapture(0)
#	ret, frame = cap.read()
	image = cv2.imread('jpeg.jpg',-1) 
	cv2.cvtColor( frame, cv2.COLOR_RGB2GRAY )
	img = br.cv2_to_imgmsg(image, encoding="passthrough")
	string = rospy.Publisher("image",Image,queue_size=100)

	rospy.init_node('image_pub')
	r=rospy.Rate(10)
	n=0
	while not rospy.is_shutdown() and n<1000:
		h = Header()
		h.stamp = rospy.Time.now()
		img.header.stamp = rospy.Time.now()
		string.publish(img)
		n=n+1
		r.sleep()


if __name__ == '__main__':
        main()

