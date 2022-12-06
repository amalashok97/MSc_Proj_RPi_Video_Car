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
print check_output(['hostname','-I'])
wlan_ip = check_output(['hostname','-I'])

filetext = open("help.txt","a")

def helpmessage(data):
#	now = rospy.Time.now()
#	timestamp = str(data.header.stamp.secs)+'.'+str(data.header.stamp.nsecs)
#	timestamp2 = str(now.secs) + "." +str(now.nsecs)
	#filetext.write(" start: " + timestamp2)
#	filetext.write(str(float(timestamp2)-float(timestamp)))
#	filetext.write("/n")
	global batteryw
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




def main():

	#get help message
	help = rospy.Subscriber("help", Help, helpmessage)
	rospy.init_node('help_message_2')
	r=rospy.Rate(10)
	battery.start_drain()



if __name__ == '__main__':
        main()

