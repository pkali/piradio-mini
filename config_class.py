#!/usr/bin/env python
#
# Raspberry Pi Internet Radio Class
# $Id: config_class.py,v 1.32 2016/07/23 13:21:28 bob Exp $
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# This class reads the /etc/radiod.conf file for configuration parameters
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#	     The authors shall not be liable for any loss or damage however caused.
#

import os
import sys
import ConfigParser
from log_class import Log

# System files
ConfigFile = "/etc/radiod.conf"

log = Log()
config = ConfigParser.ConfigParser()


class Configuration:
	# Input source
	RADIO = 0
	PLAYER = 1
	PANDORA = 2
	LIST = 0
	STREAM = 1

	# Rotary class selection
	STANDARD = 0	# Select rotary_class.py
	ALTERNATIVE = 1	# Select rotary_class_alternative.py

	# Configuration parameters
	mpdport = 6600  # MPD port number
	dateFormat = "%H:%M %d/%m/%Y"   # Date format
	#volume_range = 100 		# Volume range 10 to 100
	volume_min = 0
	volume_max = 100
	volume_increment = 4
	display_playlist_number = False # Two line displays only, display station(n)
	source = RADIO  # Source RADIO or Player
	stationNamesSource = LIST # Station names from playlist names or STREAM
	rotary_class = STANDARD		# Rotary class STANDARD or ALTERNATIVE

	# Remote control parameters 
	remote_led = 0  # Remote Control activity LED 0 = No LED	
	remote_control_host = 'localhost' 	# Remote control to radio communication port
	remote_listen_host = 'localhost' 	# Remote control to radio communication port
	remote_control_port = 5100 	  	# Remote control to radio communication port

	ADAFRUIT = 1	    # I2C backpack type AdaFruit
	PCF8574  = 2	    # I2C backpack type PCF8574
	i2c_backpack = ADAFRUIT 
	i2c_address = 0x00	# Use defaults or use setting in radiod.conf 
	backpack_names = [ 'UNKWOWN','ADAFRUIT','PCF8574']
	speech = False 	    # Speech on for visually impaired or blind persons
	isVerbose = False     # Extra speech verbosity
	speech_volume = 80  # Percentage speech volume 
	use_playlist_extensions = False # MPD 0.15 requires playlist.<ext>
	rss = False	# RSS in standby mode (Pecus)
	bright = True	# LCD high brightness (Pecus)
	media_update = False	# always update media library (Pecus)
	pandora_available = False	# is Pandora accout available ? (Pecus)
	force_streaming = False	# If True, streaming is possible even on weak raspberries (1 core)

	# Colours for Adafruit LCD
	color = { 'OFF': 0x0, 'RED' : 0x1, 'GREEN' : 0x2, 'YELLOW' : 0x3,
		  'BLUE' : 0x4, 'VIOLET' : 0x5, 'TEAL' : 0x6, 'WHITE' : 0x7 }

	colorName = { 0: 'Off', 1 : 'Red', 2 : 'Green', 3 : 'Yellow',
		    4 : 'Blue', 5 : 'Violet', 6 : 'Teal', 7 : 'White' }

	colors = { 'bg_color' : 0x0,
		   'mute_color' : 0x0,
		   'shutdown_color' : 0x0,
		   'error_color' : 0x0,
		   'search_color' : 0x0,
		   'source_color' : 0x0,
		   'info_color' : 0x0,
		   'menu_color' : 0x0,
		   'sleep_color': 0x0 }

	# List of loaded options for display
	configOptions = {}

	# Other definitions
	UP = 0
	DOWN = 1

	#  GPIOs for switches and rotary encoder configuration
	switches = { "menu_switch": 25,
		     "mute_switch": 4,
		     "left_switch": 14,
		     "right_switch": 15,
		     "up_switch": 17,
		     "down_switch": 18,
		   }

	#  GPIOs for LCD connections
	lcdconnects = { 
		     "lcd_enable": 8,
		     "lcd_select": 7,
		     "lcd_data4": 27,
		     "lcd_data5": 22,
		     "lcd_data6": 23,
		     "lcd_data7": 24,
		     "lcd_bri": 10,
		   }

	# Initialisation routine
	def __init__(self):
		log.init('radio')
		if not os.path.isfile(ConfigFile) or os.path.getsize(ConfigFile) == 0:
			log.message("Missing configuration file " + ConfigFile, log.ERROR)
		else:
			self.getConfig()

		return

	# Get configuration options from /etc/radiod.conf
	def getConfig(self):
		section = 'RADIOD'

		# Get options
		config.read(ConfigFile)
		try:
			options =  config.options(section)
			for option in options:
				parameter = config.get(section,option)
				msg = "Config option: " + option + " = " + parameter
				
				self.configOptions[option] = parameter

				if option == 'loglevel':
					next

				#elif option == 'volume_range':
				#	range = int(parameter)
				#	if range < 10:
				#		range = 10
				#	if range > 100:
				#		range = 100
				#	self.volume_range = range
				#	self.volume_increment = int(range/21)

				elif option == 'volume_min':
					if int(parameter) < 0:
						self.volume_min = 0
					else:
						self.volume_min = int(parameter)

				elif option == 'volume_max':
					if int(parameter) > 100:
						self.volume_max = 100
					else:
						self.volume_max = int(parameter)

				elif option == 'remote_led':
					self.remote_led = int(parameter)

				elif option == 'remote_control_host':
					self.remote_control_host = parameter

				elif option == 'remote_control_port':
					self.remote_control_port = int(parameter)

				elif option == 'remote_listen_host':
					self.remote_listen_host = parameter

				elif option == 'mpdport':
					self.mpdport = int(parameter)

				elif option == 'dateformat':
					self.dateFormat = parameter

				elif option == 'display_playlist_number':
					if parameter == 'yes':
						self.display_playlist_number = True

				elif option == 'startup':
					if parameter == 'MEDIA':
						self.source =  self.PLAYER
					elif parameter == 'PANDORA':
						self.source =  self.PANDORA

				elif option == 'station_names':
					if parameter == 'stream':
						self.stationNamesSource =  self.STREAM
					else:
						self.stationNamesSource =  self.LIST

				elif option == 'i2c_backpack':
					if parameter == 'PCF8574':
						self.i2c_backpack =  self.PCF8574
					else:
						self.i2c_backpack =  self.ADAFRUIT

				elif option == 'i2c_address':
					value = int(parameter,16)
					if parameter  > 0x00:
						self.i2c_address =  value

				elif 'color' in option:
					try:
						self.colors[option] = self.color[parameter]
					except:
						log.message("Invalid option " + option + ' ' + parameter, log.ERROR)

				elif option == 'speech':
					if parameter == 'yes':
						self.speech = True
					else:
						self.speech = False

				elif option == 'verbose':
					if parameter == 'yes':
						self.isVerbose = True
					else:
						self.isVerbose = False

				elif option == 'speech_volume':
					self.speech_volume = int(parameter)

				elif option == 'use_playlist_extensions':
					if parameter == 'yes':
						self.use_playlist_extensions = True
					else:
						self.use_playlist_extensions = False

				elif '_switch' in option:
					switch = int(parameter)
					try:
						self.switches[option] = switch
					except:
						msg = "Invalid switch parameter " +  option
						log.message(msg,log.ERROR)

				elif 'lcd_' in option:
					lcdconnect = int(parameter)
					try:
						self.lcdconnects[option] = lcdconnect
					except:
						msg = "Invalid LCD connect parameter " +  option
						log.message(msg,log.ERROR)

				elif option == 'rotary_class':
					if parameter == 'standard':
						self.rotary_class = self.STANDARD
					else:
						self.rotary_class = self.ALTERNATIVE

				elif option == 'rss':		# option for RSS in standby mode (Pecus)
					if parameter == 'yes':	# (Pecus)
						self.rss = True		# (Pecus)
					else:		# (Pecus)
						self.rss = False	# (Pecus)

				elif option == 'bright':		# option for high brightness of LCD (Pecus)
					if parameter == 'yes':	# (Pecus)
						self.bright = True		# (Pecus)
					else:		# (Pecus)
						self.bright = False	# (Pecus)

				elif option == 'media_update':		# option for update media library (Pecus)
					if parameter == 'yes':	# (Pecus)
						self.media_update = True		# (Pecus)
					else:		# (Pecus)
						self.media_update = False	# (Pecus)

				elif option == 'pandora_available':		# option for Pandora availablity (Pecus)
					if parameter == 'yes':	# (Pecus)
						self.pandora_available = True		# (Pecus)
					else:		# (Pecus)
						self.pandora_available = False	# (Pecus)

				elif option == 'force_streaming':		# option for streaming availablity on 1 core raspberries (Pecus)
					if parameter == 'yes':	# (Pecus)
						self.force_streaming = True		# (Pecus)
					else:		# (Pecus)
						self.force_streaming = False	# (Pecus)


				else:
					msg = "Invalid option " + option + ' in section ' \
						+ section + ' in ' + ConfigFile
					log.message(msg,log.ERROR)

			if self.source == self.PANDORA:
				if not self.pandora_available:
					self.source = self.RADIO

			range = self.volume_max - self.volume_min
			if range < 22:
				self.volume_min = 0
				sel.volume_max = 100
				range = 100
			self.volume_increment = int(range/21)
		except ConfigParser.NoSectionError:
			msg = ConfigParser.NoSectionError(section),'in',ConfigFile
			log.message(msg,log.ERROR)
		return

	# Get routines
	
	# Get I2C backpack type
	def getBackPackType(self):
		return self.i2c_backpack

	# Get I2C backpack address
	def getI2Caddress(self):
		return self.i2c_address

	# Get I2C backpack name
	def getBackPackName(self):
		return self.backpack_names[self.i2c_backpack]

	# Get the volume range
	#def getVolumeRange(self):
	#	return self.volume_range

	def getVolumeMax(self):
		return self.volume_max

	def getVolumeMin(self):
		return self.volume_min

	# Get the volume increment
	def getVolumeIncrement(self):
		return self.volume_increment

	# Get the remote control activity LED number
	def getRemoteLed(self):
		return self.remote_led

	# Get the remote Host default localhost
	def getRemoteUdpHost(self):
		return self.remote_control_host

	# Get the UDP server listener IP Host default localhost
	# or 0.0.0.0 for all interfaces
	def getRemoteListenHost(self):
		return self.remote_listen_host

	# Get the remote Port  default 5100
	def getRemoteUdpPort(self):
		return self.remote_control_port

	# Get the mpdport
	def getMpdPort(self):
		return self.mpdport

	# Get the date format
	def getDateFormat(self):
		return self.dateFormat

	# Get display playlist number (Two line displays only)
	def getDisplayPlaylistNumber(self):
		return self.display_playlist_number

	# Get the startup source 0=RADIO or 1=MEDIA
	def getSource(self):
		return self.source

	# Get the startup source name RADIO MEDIA
	def getSourceName(self):
		source_name = "MEDIA"
		if self.getSource() < 1:
			source_name = "RADIO"
		return source_name

	# Get the background color (Integer)
	def getBackColor(self,sColor):
		color = 0x0
	# Get the remote Port  default 5100
	def getRemoteUdpPort(self):
		return self.remote_control_port

	# Get the mpdport
	def getMpdPort(self):
		return self.mpdport

	# Get the date format
	def getDateFormat(self):
		return self.dateFormat

	# Get display playlist number (Two line displays only)
	def getDisplayPlaylistNumber(self):
		return self.display_playlist_number

	# Get the startup source 0=RADIO or 1=MEDIA
	def getSource(self):
		return self.source

	# Get the startup source name RADIO MEDIA
	def getSourceName(self):
		source_name = "MEDIA"
		if self.getSource() < 1:
			source_name = "RADIO"
		return source_name

	# Get the background color (Integer)
	def getBackColor(self,sColor):
		color = 0x0
		try: 
			color = self.colors[sColor]
		except:
			log.message("Invalid option " + sColor, log.ERROR)
		return color

	# Cycle background colors
	def cycleColor(self,direction):
		color = self.getBackColor('bg_color')

		if direction == self.UP:
			color += 1
		else:
			color -= 1

		if color < 0:
			color = 0x7
		elif color > 0x7:
			color = 0x0

		self.colors['bg_color'] = color
		return color


	# Get the background colour string name
	def getBackColorName(self,iColor):
		sColor = 'None' 
		try: 
			sColor = self.colorName[iColor]
		except:
			log.message("Invalid option " + int(iColor), log.ERROR)
		return sColor

	# Get speech
	def getSpeech(self):
		return self.speech	

	# Get verbose
	def verbose(self):
		return self.isVerbose
	
	# Get RSS mode (Pecus)
	def getRss(self):        # (Pecus)
		return self.rss  # (Pecus)

	# Get LCD brightness mode (Pecus)
	def getBright(self):        # (Pecus)
		return self.bright  # (Pecus)

	# Get always media update flag (Pecus)
	def getAlwaysUpdate(self):        # (Pecus)
		return self.media_update  # (Pecus)

	# Get pandora flag (Pecus)
	def getPandoraAvailable(self):        # (Pecus)
		return self.pandora_available  # (Pecus)

		# Get streaming flag (Pecus)
	def getForceStreaming(self):        # (Pecus)
		return self.force_streaming  # (Pecus)

	# Get speech volume % of normal volume level
	def getSpeechVolume(self):
		return self.speech_volume

	# Get playlist extensions used 
	def getPlaylistExtensions(self):
		return self.use_playlist_extensions	

	# Return the station name source (Stream or playlist)
	def getStationNamesSource(self):
		return self.stationNamesSource	

	# Display parameters
	def display(self):
		for option in self.configOptions:
			param = self.configOptions[option]
			if option != 'None':
				log.message(option + " = " + param, log.DEBUG)
		return

	# Return the ID of the rotary class to be used STANDARD or ALTERNATIVE
	def getRotaryClass(self):
		return self.rotary_class

	# Returns the switch GPIO configuration by label
	def getSwitchGpio(self,label):
		switch = -1
		try:
			switch = self.switches[label]
		except:
			msg = "Invalid switch label " + label
			log.message(msg, log.ERROR)
		return switch

	# Returns the LCD GPIO configuration by label
	def getLcdGpio(self,label):
		switch = -1
		try:
			lcdconnect = self.lcdconnects[label]
		except:
			msg = "Invalid LCD connection label " + label
			log.message(msg, log.ERROR)
		return lcdconnect

# End Configuration of class

# Test Configuration class
if __name__ == '__main__':

	config = Configuration()
	print "Configuration file", ConfigFile
	#print "Volume range:", config.getVolumeRange()
	print "Volume min.:", config.getVolumeMin()
	print "Volume max.:", config.getVolumeMax()
	print "Volume increment:", config.getVolumeIncrement()
	print "Mpd port:", config.getMpdPort()
	print "Remote LED:", config.getRemoteLed()
	print "Remote LED port:", config.getRemoteUdpPort()
	print "Date format:", config.getDateFormat()
	print "Display playlist number:", config.getDisplayPlaylistNumber()
	print "Source:", config.getSource(), config.getSourceName()
	print "Background colour number:", config.getBackColor('bg_color')
	print "Background colour:", config.getBackColorName(config.getBackColor('bg_color'))
	print "Speech:", config.getSpeech()
	print "Speech volume:", str(config.getSpeechVolume()) + '%'
	print "Verbose:", config.verbose()
	print "RRS in standby:", config.getRss()  # (Pecus)
	print "LCD high brightness:", config.getBright()  # (Pecus)
	print "Always update media library:", config.getAlwaysUpdate()  # (Pecus)
	print "Pandora account available:", config.getPandoraAvailable()  # (Pecus)
	print "Streaming on 1 core raspberries:",config.getForceStreaming()	# (Pecus)
	if config.getStationNamesSource() is 1:
		sSource = "STREAM"
	else: 
		sSource = "LIST"
	print "Station names source:",sSource
	print "Use playlist extensions:", config.getPlaylistExtensions()

	for switch in config.switches:
		print switch, config.getSwitchGpio(switch)
	
	for lcdconnect in sorted(config.lcdconnects):
		print lcdconnect, config.getLcdGpio(lcdconnect)
	
	rclass = ['Standard', 'Alternative']
	rotary_class = config.getRotaryClass()
	print "Rotary class:", rotary_class, rclass[rotary_class]
	print "Backpack type:", config.getBackPackType(), config.getBackPackName()
	print "I2C address:", hex(config.getI2Caddress())

# End of file

