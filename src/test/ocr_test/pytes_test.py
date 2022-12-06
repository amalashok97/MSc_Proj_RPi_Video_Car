#!/usr/bin/python

import sys
import Image
import pytesseract
import rospy
import time
import cv2
import psutil
import time


filetimes = open("pytes/box_text.txt","a")
filetext = open("pytes/box_times.txt","a")
def main():
	n=0
	while not rospy.is_shutdown() and n<300:
		cpu_before=psutil.cpu_percent(interval=1.0)
		starttime=time.time() #rospy.Time.now()
		text =pytesseract.image_to_string(Image.open("grey_box.jpg"))
		time2 = time.time()
		cpu_used=psutil.cpu_percent(interval=None)
		filetext.write(text.encode("utf-8"))
		filetimes.write(str(cpu_used)+ "," +str(time2 - starttime)+"\n")
		time.sleep(1)
		filetext.write("\n-------------\n")
		n+=1

if __name__ == '__main__':
        main()

