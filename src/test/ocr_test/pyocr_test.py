#!/usr/bin/python

import sys
import Image
import pyocr
import pyocr.builders
import rospy
import time
import cv2
import psutil
import time
import codecs

filetimes = open("pyocr/sign_times.txt","a")
filetext = open("pyocr/sign_text.txt","a")
def main():
	n=0
	tools = pyocr.get_available_tools()
	if len(tools)==0:
		print("No ocr tool available")
		sys.exit()
	tool = tools[0]
	buildern = pyocr.builders.TextBuilder()
	while not rospy.is_shutdown() and n<300:
		cpu_before=psutil.cpu_percent(interval=1.0)
		starttime=time.time() #rospy.Time.now()

		text =tool.image_to_string(Image.open("sign.jpg"), lang="eng", builder=pyocr.builders.TextBuilder())
		#print text

		time2 = time.time()
		cpu_used=psutil.cpu_percent(interval=None)
		filetext.write(text.encode('utf-8'))
		filetext.write("\n--------------------\n")
		filetimes.write(str(cpu_used)+ "," +str(time2 - starttime)+"\n")
		time.sleep(1)
		n+=1

if __name__ == '__main__':
        main()

