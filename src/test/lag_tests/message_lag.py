#!/usr/bin/python
import rospy
import time
import random,string
from qr_tracker.msg import TestString
from std_msgs.msg import Header
def main():

	strings = rospy.Publisher("basic",TestString,queue_size=10)
	rospy.init_node('node_name_1')
	r=rospy.Rate(10)
	n=0
	out_string = ''.join(random.choice(string.lowercase) for x in range(15))
	while not rospy.is_shutdown() and n<1000:
		hed = Header()
		hed.stamp = rospy.Time.now()
		
		msg = TestString(h=hed,string="Start")

#		msg.header.stamp = rospy.Time.now()
		n=n+1
		strings.publish(msg)
		r.sleep()
	

if __name__ == '__main__':
        main()

