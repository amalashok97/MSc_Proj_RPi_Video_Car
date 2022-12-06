#!/usr/bin/python

import sys
import Image
import tesserocr
import rospy
import time
import cv2
import psutil
import time

#p=psutil.Process()

filetimes = open("tesser/sign_times.txt","a")
filetext = open("tesser/sign_text.txt","a")

def main():
	n=0
	while not rospy.is_shutdown() and n<300:
		cpu_before=psutil.cpu_percent(interval=1.0)
		starttime=time.time() #rospy.Time.now()
		text =tesserocr.image_to_text(Image.open("sign.jpg"))
		time2 = time.time()
		cpu_used=psutil.cpu_percent(interval=None)
		filetext.write(text.encode("utf-8"))
		filetimes.write(str(cpu_used)+ "," +str( time2-starttime)+"\n")
		filetext.write("\n----------\n")
		n+=1

if __name__ == '__main__':
        main()

