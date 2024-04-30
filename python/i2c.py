from smbus import SMBus
import gpiod

addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

calFlagPin = 17  # GPIO 17, physical pin 11
chip = gpiod.chip('gpiochip4')
calFlagLine = chip.get_line(calFlagPin)
calFlagLine.request()

config = gpiod.line_request(calFlagLine,gpiod.line_request.DIRECTION_OUTPUT,0)
config.consumer = "Arduino"
# config.request_type = gpiod.line_request.DIRECTION_OUTPUT
# calFlagLine.set_value(0)

# chip = gpiod.chip(LED_CHIP)
# led = chip.get_line(LED_LINE_OFFSET)

# config = gpiod.line_request()
# config.consumer = "Blink"
# config.request_type = gpiod.line_request.DIRECTION_OUTPUT

calibrate = False
while True:
	
	mode = input("What mode would you like to run?\n[cal] [step] [hold] [per] [abs]\n>>>>    ")
	
	if mode == "cal":
		print("Entering calibration mode")
		calFlagLine.set_value(1)
		calLoop = True
		while calLoop:
			calIn = input("Enter relative angle or [exit]: ")
			if calIn == "exit": 
				calLoop == False
				break
			else: print(calIn)
			bus.write_byte(addr,int(calIn))
		print("Exitting calibration mode...")
		calFlagLine.set_value(0)

	elif mode == "abs":
		print("Entering absolute position mode")
		absLoop = True
		while absLoop:
			absIn = input("Enter absolute angle in degrees or [exit]: ")
			if absIn == "exit": 
				absLoop = False
				break
			else: print(int(absIn))
			bus.write_byte(addr,int(absIn))
		print("Exitting absolute position mode...")

	else:
		mode = input("invalid input\nWhat mode would you like to run?\n[cal] [step] [hold] [per] [abs]\n>>>>    ")

calFlagLine.release()

#  https://dronebotworkshop.com
#  https://dronebotworkshop.com/i2c-arduino-raspberry-pi/
#  https://roboticsbackend.com/raspberry-pi-master-arduino-slave-i2c-communication-with-wiringpi/
