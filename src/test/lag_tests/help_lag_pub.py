#!/usr/bin/python
import rospy
import time
import os
import psutil

from qr_tracker.msg import Help
from std_msgs.msg import Header

from virtual_battery import VirtualBattery
DISCHARGE_INTERVAL = 10
battery = VirtualBattery(discharge_interval=DISCHARGE_INTERVAL)

#setting this ip
from subprocess import check_output
#print check_output(['hostname','-I'])
wlan_ip = check_output(['hostname','-I'])

filetext = open("help_return.txt","a")
finished = True
starttime = ""

def help_return(data):
	global finished,starttime
	
	timestamp = starttime
	t = rospy.Time.now()
	timestamp2 = str(t.secs) + "." +str(t.nsecs)
	filetext.write(str(float(timestamp2) - float(timestamp)))
	filetext.write("\n")
	finished=True

def main():
	global finished,starttime
	help_top = rospy.Publisher("help",Help,queue_size=100)
	rospy.sleep(1)
	helpret = rospy.Subscriber("help_ret",Help,help_return)
	rospy.init_node('help_lag_pub')
	r=rospy.Rate(10)
	n=0
	battery.start_drain()
	while not rospy.is_shutdown() and n<100:
		if finished==True:
			h = Header()
			h.stamp = rospy.Time.now()
			starttime = str(h.stamp.secs) + "." +str(h.stamp.nsecs)
			filetext.write("start: " +timestamp2)
			cpu_percent =100- psutil.cpu_percent(interval=None, percpu=False)
			process = psutil.Process(os.getpid())
			mem = str(process.memory_percent())
			bat=str(battery.battery_percentage())
		#publish along with ip of robot to return it to and this ip
			help_top.publish(h,wlan_ip,str(cpu_percent),bat,mem, wlan_ip)
			finished=False
			n=n+1
			#r.sleep()


if __name__ == '__main__':
        main()

