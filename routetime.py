#!/usr/bin/python
# Route Time
# Displays leave and return time for city routes
# Parts needed LCD Pi Plate, 4 7 segment displays

# ! Imports
import Adafruit_CharLCD as LCD
from Adafruit_LED_Backpack import SevenSegment
import Adafruit_Trellis


# Trellis setup
# Momentary mode LED lights only when pressed
# Latching mode LED lights on/off when pressed
MOMENTARY = 0
LATCHING = 1
# Will need to set this mode by what data is being entered
MODE = MOMENTARY

matrix0 = Adafruit_Trellis.Adafruit_Trellis()
trellis = Adafruit_Trellis.Adafruit_TrellisSet(matrix0)
# Number of Trellis Boards
NUMTRELLIS = 1

numKeys = NUMTRELLIS * 1

I2C_BUS = 1

trellis.begin((0x75, I2C_BUS))


# Initialize 7-Segment Matrix Displays
display1 = SevenSegment.SevenSegment(address=0x71)
display2 = SevenSegment.SevenSegment(address=0x72)
display3 = SevenSegment.SevenSegment(address=0x73)
display4 = SevenSegment.SevenSegment(address=0x74)

display1.begin()
display2.begin()
display3.begin()
display4.begin()

colon = True

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDPlate()

# Custom characters used on display for
# Directional buttons Up(1), Down(3), Left(4), Right(2)
# As well as Select(5)
# In order as shown
# ! Custom Characters
lcd.create_char(1, [0,0,4,14,31,0,0,0])
lcd.create_char(2, [0,8,12,14,12,8,0,0])
lcd.create_char(3, [0,0,31,14,4,0,0,0])
lcd.create_char(4, [0,2,6,14,6,2,0,0])
lcd.create_char(5, [0,0,10,0,17,14,0,0])

# Clear the LCD screen, set the color to blue and set the initial message
lcd.clear()
lcd.set_color(0.0, 0.0, 1.0)
lcd.message('Leave/Return\n\x01\x03 C1 & \x02\x04 C2 \x05 Toggle')
	
# Wait for button press to set times
# Then enter text via USB or wireless keyboard
# LCD Plate directional buttons for Leave/Return times
# Select button currently unused
# Green color for Leave times, Red for Return while clear LCD before entry
# And have LCD display cursor and blink menacingly
# ! Main Loop
while True:
# Set Select to swap from Momentary to Latching
	if lcd.is_pressed(LCD.SELECT):
		lcd.clear()
		lcd.blink(True)
		lcd.show_cursor(True)
		lcd.set_color(1.0, 1.0, 0.0)
		MODE = LATCHING
		lcd.message('Set to %s') % MODE
	else:
		MODE = MOMENTARY
	if lcd.is_pressed(LCD.UP):
		lcd.clear()
		lcd.blink(True)
		lcd.show_cursor(True)
		lcd.set_color(0.0, 1.0, 0.0)
		lcd.message('Enter C1 Start Time\n')
		display1.clear()
		display1.set_colon(True)
		c1up = float(raw_input())
		lcd.message(c1up)
		display1.print_float(c1up, 0)
		display1.write_display()
	if lcd.is_pressed(LCD.RIGHT):
		lcd.clear()
		lcd.blink(True)
		lcd.show_cursor(True)
		lcd.set_color(0.0, 1.0, 0.0)
		c2right = float(raw_input('C2 Start Time\n'))
		display3.clear()
		display3.print_float(c2right,0)
		display3.set_colon(True)
		display3.write_display()
		lcd.message('c2right')
	if lcd.is_pressed(LCD.DOWN):
		lcd.clear()
		lcd.blink(True)
		lcd.show_cursor(True)
		lcd.set_color(1.0, 0.0, 0.0)
		c1down = float(raw_input('C1 Return Time\n'))
		display2.clear()
		display2.print_float(c1down,0)
		display2.set_colon(True)
		display2.write_display()
		lcd.message('c1down')
	if lcd.is_pressed(LCD.LEFT):
		lcd.clear()
		lcd.blink(True)
		lcd.show_cursor(True)
		lcd.set_color(1.0, 0.0, 0.0)
		c2left = float(raw_input('C2 Return Time\n'))
		display4.clear()
		display4.print_float(c2left,0)
		display4.set_colon(True)
		display4.write_display()
		lcd.message('c2left')
		time.sleep(0.03)
	if MODE == MOMENTARY:
		# If a button was just pressed or released...
		if trellis.readSwitches():
			# go through every button
			for i in range(numKeys):
				# if it was pressed, turn it on
				if trellis.justPressed(i):
					print 'v{0}'.format(i)
					trellis.setLED(i)
				# if it was released, turn it off
				if trellis.justReleased(i):
					print '^{0}'.format(i)
					trellis.clrLED(i)
			# tell the trellis to set the LEDs we requested
			trellis.writeDisplay()

	if MODE == LATCHING:
		# If a button was just pressed or released...
		if trellis.readSwitches():
			# go through every button
			for i in range(numKeys):
				# if it was pressed...
				if trellis.justPressed(i):
					print 'v{0}'.format(i)
					# Alternate the LED
					if trellis.isLED(i):
						trellis.clrLED(i)
					else:
						trellis.setLED(i)
			# tell the trellis to set the LEDs we requested
			trellis.writeDisplay()

