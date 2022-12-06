#!/usr/bin/python
# Initial QR-detecting script.
# !!! Does not use the default python zbar !!!
# Instead it uses https://github.com/zplab/zbar-py, since this wrapper also
# allows for code location to be returned

import cv2
#cv2.namedWindow('Result', cv2.WINDOW_AUTOSIZE)
import sys
import numpy as np
import Image
import threading
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
import time
import zbar
import motor
import motor_direction
import camera_direction
import rospy

pan_threshold = 150
tilt_threshold = 150
delay_interval = 1
motor_runtime = 0.3

cap = None


		
class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			self.QR_detector(0)
			return
		if self.path.endswith('.html'):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="10.42.0.194:8080/cam.mjpg"/>')
			self.wfile.write('</body></html>')
			return
	def stream_image(self, image):
		jpg = Image.fromarray(image)
		tmpFile = StringIO.StringIO()
		jpg.save(tmpFile,'JPEG')
		self.wfile.write("--jpgboundary")
		self.send_header('Content-type','image/jpeg')
		self.send_header('Content-length',str(tmpFile.len))
		self.end_headers()
		jpg.save(self.wfile,'JPEG')
		time.sleep(0.05)
	
	def QR_detector(self, device_ID):
		global cap
		cap = cv2.VideoCapture(device_ID)
	
		while not rospy.is_shutdown():
			# Capture frame-by-frame
			try:
				ret, frame = cap.read()
				cv2.rectangle(frame, (220, 140), (420, 340), (255, 0, 0), 2)
	
				image = cv2.cvtColor( frame, cv2.COLOR_RGB2GRAY )
				scanner = zbar.Scanner()
				results = scanner.scan(image)
	
				for result in results:
					print "Processing results: ",len(results)
					must_move = 0
					#print(result.type, result.data, result.quality, result.position)
					cv2.rectangle(image, result.position[0], result.position[2], (255, 255, 255), 2)
					renderpt = ((result.position[1][0]+result.position[2][0])/2+90, (result.position[1][1]+result.position[2][1])/2)
					cv2.putText(image, result.data, renderpt, cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
					code_size = result.position[1][1]-result.position[0][1]
	
					
					move_direction = 'f' if code_size<100 else ('b' if code_size>300 else 0)
						#print "Not optimal distance from code."
	
					frame_centre_x = image.shape[1]/2
					frame_centre_y = image.shape[0]/2
					code_centre_x = (result.position[0][0]+result.position[2][0])/2
					code_centre_y = (result.position[0][1]+result.position[2][1])/2
					correction_x = frame_centre_x - code_centre_x
					correction_y = frame_centre_y - code_centre_y
	
					pan_degree = correction_x if abs(correction_x)>pan_threshold else 0
					tilt_degree = correction_y if abs(correction_y)>tilt_threshold else 0
					self.code_refocus(move_direction, pan_degree, tilt_degree)
					#if must_move:
						#print "Moving..."+"forwards" if 200-code_size>0 else "backwards"
						
						#motor_direction.turn(correction_x)
						#motor.stop()
						#camera_direction.home()
	
					#if abs(correction_y)>tilt_threshold and must_move:
						#camera_direction.tilt(correction_y)
						#motor_direction.turn(correction_x)
						#motor.motor_control('f' if 200-code_size>0 else 'b')
						#camera_direction.home()
				self.stream_image(image)
			except KeyboardInterrupt:
				break
	
			# cv2.imshow('Video', frame)
			# key = cv2.waitKey(1)
			# if key != -1 and key == ord('q'):
			# 	cap.release()
			# 	cv2.destroyAllWindows()
			# 	sys.exit()
	
	def code_refocus(self, move_direction, pan_degree, tilt_degree):
		if move_direction:
			if pan_degree:
				self.move_camera("pan", pan_degree)
				self.turn_wheels(pan_degree)
				self.move_wheels(move_direction)
				self.turn_wheels("home")
			if tilt_degree:
				self.move_camera("tilt", tilt_degree)
			elif not pan_degree:
				self.move_wheels(move_direction)

		else:
			if pan_degree:
				self.move_camera("pan", pan_degree)
			if tilt_degree:
				self.move_camera("tilt", tilt_degree)
	
	def turn_wheels(self, angle):
		if angle=="home":
			motor_direction.home()
		else:
			motor_direction.turn(angle)
		
	def move_wheels(self, direction):
		time.sleep(delay_interval)
		motor.motor_control(direction)
		time.sleep(motor_runtime)
		motor.stop()

	def move_camera(self, movement, step):
		time.sleep(delay_interval)
		if movement=="pan":
			camera_direction.pan(25*np.sign(step))
		if movement=="tilt":
			camera_direction.tilt(25*np.sign(step))			
		time.sleep(delay_interval)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""

def main():
	rospy.init_node("qr_tracker", disable_signals=True)
	motor.setup()
	motor_direction.setup()
	#motor_direction.home()
	camera_direction.setup()
	camera_direction.home()
	try:
		server = ThreadedHTTPServer(('10.42.0.194', 8080), CamHandler)
		print "server started"
		server.serve_forever()
	except KeyboardInterrupt:
		print "Terminating program..."
		cap.release()
		server.socket.close()


if __name__ == '__main__':
	main()
