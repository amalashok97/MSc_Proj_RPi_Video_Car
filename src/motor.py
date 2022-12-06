import RPi.GPIO as GPIO
import Sunfounder_PWM_Servo_Driver.Servo_init as pwm

# ===========================================================================
# Raspberry Pi pin11, 12, 13 and 15 to realize the clockwise/counterclockwise
# rotation and forward and backward movements
# ===========================================================================
Motor0_A = 11  # pin11
Motor0_B = 12  # pin12
Motor1_A = 13  # pin13
Motor1_B = 15  # pin15

# ===========================================================================
# Set channel 4 and 5 of the servo driver IC to generate PWM, thus 
# controlling the speed of the car
# ===========================================================================
EN_M0    = 4  # servo driver IC CH4
EN_M1    = 5  # servo driver IC CH5

pins = [Motor0_A, Motor0_B, Motor1_A, Motor1_B]
# motor0_dir = 1
# motor1_dir = 1
p = pwm.init()

def set_speed(speed):
	speed *= 40
	#print 'speed is: ', speed
	p.setPWM(EN_M0, 0, speed)
	p.setPWM(EN_M1, 0, speed)

def stop():
	for pin in pins:
		GPIO.output(pin, GPIO.LOW)

def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)        # Number GPIOs by its physical location
	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)

def motor_GPIO_output(a, b):
	GPIO.output(Motor0_A, a)
	GPIO.output(Motor0_B, b)
	GPIO.output(Motor1_A, a)
	GPIO.output(Motor1_B, b)

def motor_control(direction='f', speed=50, stop=False):
	set_speed(speed)
	if not stop:
		if direction == 'f':
			#print "MOTOR: Moving forward..."
			motor_GPIO_output(GPIO.LOW, GPIO.HIGH)
		elif direction == 'b':
			#print "MOTOR: Moving backward..."
			motor_GPIO_output(GPIO.HIGH, GPIO.LOW)
		else:
			print 'Invalid direction.'
	else:
		stop()
