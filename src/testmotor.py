#!/usr/bin/python
import motor_direction
import time

def main():
	motor_direction.setup()
	motor_direction.home()
	
	print "Testing turn left... "
	motor_direction.turn(0)
	time.sleep(2)
	print "Testing turn right... "
	motor_direction.turn(255)

if __name__ == "__main__":
	main()
