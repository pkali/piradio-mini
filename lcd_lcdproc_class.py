#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# $Id: lcd_class.py,v 1.27 2016/04/06 09:48:25 bob Exp $
# Raspberry Pi Internet Radio
# using an HD44780 LCD display
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# From original LCD routines : Matt Hawkins
# Site   : http://www.raspberrypi-spy.co.uk
# Timing improvements fromobert Coward/Paul Carpenter
# Site   : http://www.raspberrypi-spy.co.uk
#          http://www.pcserviceslectronics.co.uk
#
# Expanded to use 4 x 20  display
#
# This program uses  Music Player Daemon 'mpd'and it's client 'mpc'
# See http://mpd.wikia.com/wiki/Music_Player_Daemon_Wiki
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#             The authors shall not be liable for any loss or damage however caused.
#

import os
import time
import RPi.GPIO as GPIO
from translate_class import Translate
from config_class import Configuration
from lcdproc.server import Server

server=Server()

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

# Define GPIO to LCD mapping
##LCD_RS = 7
##LCD_E  = 8
##LCD_D4_21 = 21    # Rev 1 Board
##LCD_D4_27 = 27    # Rev 2 Board
##LCD_D5 = 22
##LCD_D6 = 23
##LCD_D7 = 24
#lcd_bri = 10	# Brightness control (Pecus)

# Define LCD device constants
LCD_WIDTH = 20    # Default characters per line
##LCD_CHR = True
##LCD_CMD = False

LCD_LINE_1 = 1
LCD_LINE_2 = 2
LCD_LINE_3 = 3
LCD_LINE_4 = 4

# Some LCDs use different addresses (16 x 4 line LCDs)
# Comment out the above two lines and uncomment the two lines below
# LCD_LINE_3 = 0x90 # LCD RAM address for the 3rd line
# LCD_LINE_4 = 0xD0 # LCD RAM address for the 4th line

# If using a 4 x 16 display also amend the lcd.setWidth(<width>) statement in rradio4.py

# Timing constants

translate = Translate()

# Temporary files for displayed text. /tmp is a tempfs in RAM (Pecus)
# Remember! If you don't want to kill your SD card, add line in /etc/fstab : (Pecus)
# 'tmpfs     /tmp      /tmpfs    size=10M,noatime   0  0'  (Pecus)
Line1File = "/tmp/radiod/line1.txt"  # (Pecus)
Line2File = "/tmp/radiod/line2.txt"  # (Pecus)
Line3File = "/tmp/radiod/line3.txt"  # (Pecus)
Line4File = "/tmp/radiod/line4.txt"  # (Pecus)


# Lcd Class 
class Lcd_lcdproc:
	width = LCD_WIDTH
	# If display can support umlauts set to True else False
        RawMode = False         # Test only
        ScrollSpeed = 0.25       # Default scroll speed

	def __init__(self):
		# Create files for displayed texts (Pecus)
		if not os.path.isdir("/tmp/radiod/"): # (Pecus)
			os.mkdir ("/tmp/radiod/") # (Pecus)
		self.writeToFile (Line1File,"1") # (Pecus)
		self.writeToFile (Line2File,"2") # (Pecus)
		self.writeToFile (Line3File,"3") # (Pecus)
		self.writeToFile (Line4File,"4") # (Pecus)
		return

	# Initialise for either revision 1 or 2 boards
	def init(self,boardRevision):

		self.lcd_init()
		return

	# Initialise the display
	def lcd_init(self):
		# INIT
		server.start_session()
		self.screen = server.add_screen("Screen")
		self.screen.set_heartbeat("off")
		self.screen.set_duration(5)
		self.line1_widget = self.screen.add_scroller_widget("MyStringWidget1", text="01234567890123456789",speed=2)
		self.line2_widget = self.screen.add_scroller_widget("MyStringWidget2", text="11234567890123456789",speed=2)
		self.line3_widget = self.screen.add_scroller_widget("MyStringWidget3", text="21234567890123456789",speed=2)
		self.line4_widget = self.screen.add_scroller_widget("MyStringWidget4", text="31234567890123456789",speed=2)
		self.line1_widget.set_top(1);
		self.line2_widget.set_top(2);
		self.line3_widget.set_top(3);
		self.line4_widget.set_top(4);
		self.line1_widget.set_left(1);
		self.line2_widget.set_left(1);
		self.line3_widget.set_left(1);
		self.line4_widget.set_left(1);
		self.line1_widget.set_direction("m");
		self.line2_widget.set_direction("m");
		self.line3_widget.set_direction("m");
		self.line4_widget.set_direction("m");
		#time.sleep(0.3)		     # Allow to settle before using
		return
	 
	# Set the display width
	def setWidth(self,width):
		self.width = width
		return

	# Send string to display
	def _string(self,message,line,speed):
		s = message.ljust(self.width," ")
		if not self.RawMode:
			s = translate.toLCD(s)
		if len(s)<=20:
			speed=0

		if speed==0:
			s=s[0:19]
		else:
			s=s[0:160]+"      "


		# SET TEXT
		if line==1:
			self.line1_widget.set_text(s)
			self.line1_widget.set_speed(speed)
		elif line==2:
			self.line2_widget.set_text(s)
			self.line2_widget.set_speed(speed)
		elif line==3:
			self.line3_widget.set_text(s)
			self.line3_widget.set_speed(speed)
		else:
			self.line4_widget.set_text(s)
			self.line4_widget.set_speed(speed)
		return

	# Display Line 1 on LED
	def line1(self,text):
		self.writeToFile (Line1File,text) # (Pecus)
		# WRITE LINE 1
		self._string(text,1,0)
		return

	# Display Line 2 on LED
	def line2(self,text):
		self.writeToFile (Line2File,text) # (Pecus)
		# WRITE LINE 2
		self._string(text,2,0)
		return

	# Display Line 3 on LED
	def line3(self,text):
		self.writeToFile (Line3File,text) # (Pecus)
		# WRITE LINE 3
		self._string(text,3,0)
		return

	# Display Line 4 on LED
	def line4(self,text):
		self.writeToFile (Line4File,text) # (Pecus)
		# WRITE LINE 4
		self._string(text,4,0)
		return

	# Scroll message on line 1
	def scroll1(self,mytext,interrupt):
		self.writeToFile (Line1File,mytext) # (Pecus)
		self._scroll(mytext,LCD_LINE_1,interrupt)
		return

	# Scroll message on line 2
	def scroll2(self,mytext,interrupt):
		self.writeToFile (Line2File,mytext) # (Pecus)
		self._scroll(mytext,LCD_LINE_2,interrupt)
		return

	# Scroll message on line 3
	def scroll3(self,mytext,interrupt):
		self.writeToFile (Line3File,mytext) # (Pecus)
		self._scroll(mytext,LCD_LINE_3,interrupt)
		return

	# Scroll message on line 4
	def scroll4(self,mytext,interrupt):
		self.writeToFile (Line4File,mytext) # (Pecus)
		self._scroll(mytext,LCD_LINE_4,interrupt)
		return

	# Scroll line - interrupt() breaks out routine if True
	def _scroll(self,mytext,line,interrupt):

		# WRITE PARTICULAR LINE line
		self._string(mytext,line,2)
		print "SCROLL: " + mytext
		return

	# Set Scroll line speed - Best values are 0.2 and 0.3
	# Limit to between 0.05 and 1.0
	def setScrollSpeed(self,speed):
		#print "SCROLL SPEED: "+str(speed)
		if speed < 0.1:
			speed = 0.2
		elif speed > 1.0:
			speed = 0.3
		self.ScrollSpeed = speed
		speed=int(speed*10)
		#self.line1_widget.set_speed(speed)
		#self.line2_widget.set_speed(speed)
		#self.line3_widget.set_speed(speed)
		#self.line4_widget.set_speed(speed)
		return

	# Set raw mode on (No translation)
	def setRawMode(self,value):
		self.RawMode = value
		return

	# Clear display
	def clearDisplay(self):
		self.writeToFile (Line1File,"") # (Pecus)
		self.writeToFile (Line2File,"") # (Pecus)
		self.writeToFile (Line3File,"") # (Pecus)
		self.writeToFile (Line4File,"") # (Pecus)
		# CLEAR DISPLAY
		self._string("                    ",1)
		self._string("                    ",2)
		self._string("                    ",3)
		self._string("                    ",4)
		time.sleep(E_POSTCLEAR)
		return

	# Set brightness (Pecus)
	def setBright(self,value):
		#GPIO.output(lcd_bri, value)
		if value :
			self.screen.set_backlight("on")
		else:
			self.screen.set_backlight("off")
		return

	# Write text to file (Pecus)
	def writeToFile(self,fname,text): # (Pecus)
		file = open(fname, "w") # (Pecus)
		file.write(text) # (Pecus)
		file.close() # (Pecus)
		return # (Pecus)

# End of Lcd_lcdproc class
