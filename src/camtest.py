#!/usr/bin/python
# Initial QR-detecting script.
# !!! Does not use the default python zbar !!!
# Instead it uses https://github.com/zplab/zbar-py, since this wrapper also
# allows for code location to be returned

import sys
import cv2
#cv2.namedWindow('Result', cv2.WINDOW_AUTOSIZE)
import numpy as np
import Image
import threading
from camera_direction import current_position
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
import time
from zbar import zbar
import pytesseract
cap = None

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while True:
				try:
					# Capture frame-by-frame
					ret, frame = cap.read()
					#cv2.imshow('Video', frame)
					image = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY)
					pro_img= cv2.threshold(image, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] #cv2.medianBlur(image,3)
					scanner = zbar.Scanner()
					results = scanner.scan(pro_img)
					#print(current_position())
				
					for result in results:
						print(result.data)
						
					jpg = Image.fromarray(pro_img)
					tmpFile = StringIO.StringIO()
					
					jpg.save(tmpFile,'JPEG')
					jpg.save('jpeg.jpg')
					self.wfile.write("--jpgboundary")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(tmpFile.len))
					self.end_headers()
					jpg.save(self.wfile,'JPEG')
					time.sleep(0.05)
					#print("pytesseract")
					for n in range(0,10):

						print(pytesseract.image_to_string(Image.open("jpeg.jpg")))
				except KeyboardInterrupt:
					break
			return
		if self.path.endswith('.html'):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="http://10.42.0.194:8080/cam.mjpg"/>')
			self.wfile.write('</body></html>')
			return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""

def main():
	global cap
	cap = cv2.VideoCapture(0)
	try:
		server = ThreadedHTTPServer(('10.42.0.194', 8080), CamHandler)
		print "server started"
		server.serve_forever()
	except KeyboardInterrupt:
		print "Terminating program..."
		cap.release()
		server.socket.close()
	#key = cv2.waitKey(1)
	#if key != -1 and key == ord('q'):
	#	cap.release()
	#	cv2.destroyAllWindows()
	#	sys.exit()

if __name__ == '__main__':
	main()

