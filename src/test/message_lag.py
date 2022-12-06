#!/usr/bin/python
import rospy
import time
from std_msgs.msg import String

def main():
	
	string = rospy.Publisher("basic",String,queue_size=100)
	rospy.init_node('node_name')
	r=rospy.Rate(10)
	while not rospy.is_shutdown():
		now=rospy.Time.now()	
		string.publish(now)
		r.sleep()

if __name__ == '__main__':
        main()

