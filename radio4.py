#!/usr/bin/env python
#
# Raspberry Pi Internet Radio
# using an HD44780 LCD display
# $Id: radio4.py,v 1.111 2016/08/07 13:33:49 bob Exp $
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
# 
# This program uses  Music Player Daemon 'mpd'and it's client 'mpc' 
# See http://mpd.wikia.com/wiki/Music_Player_Daemon_Wiki
#
# 4 x 20 character LCD version
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#	     The authors shall not be liable for any loss or damage however caused.
#


import os
import RPi.GPIO as GPIO
import signal
import subprocess
import sys
import time
import socket
import string
import datetime 
from time import strftime
import shutil
import atexit
import traceback
import requests

# Class imports
from radio_daemon import Daemon
from radio_class import Radio
from lcd_class import Lcd
from log_class import Log
from rss_class import Rss
from config_class import Configuration  # for configuration read (Pecus)


# To use GPIO 14 and 15 (Serial RX/TX)
# Remove references to /dev/ttyAMA0 from /boot/cmdline.txt and /etc/inittab 

UP = 0
DOWN = 1

#CurrentStationFile = "/var/lib/radiod/current_station"
#CurrentTrackFile = "/var/lib/radiod/current_track"
#CurrentFile = CurrentStationFile
PlaylistsDirectory = "/var/lib/mpd/playlists/"


log = Log()
radio = Radio()
lcd = Lcd()
rss = Rss()
config = Configuration()	# for configuration read (Pecus)

# Signal SIGTERM handler
def signalHandler(signal,frame):
	global lcd
	global log
	radio.execCommand("umount /media > /dev/null 2>&1")
	radio.execCommand("umount /share > /dev/null 2>&1")
	pid = os.getpid()
	log.message("Radio stopped, PID " + str(pid), log.INFO)
	lcd.line1("   Radio stopped")  # center alignment (Pecus)
	lcd.line2("")
	lcd.line3("")
	lcd.line4("")
	lcd.setBright(False)  # LCD backlight brightness to low (Pecus)
	GPIO.cleanup()
	sys.exit(0)

# Daemon class
class MyDaemon(Daemon):

	def run(self):
		#global CurrentFile

		GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
		GPIO.setwarnings(False)      # Ignore warnings

		# Get switches configuration
		up_switch = radio.getSwitchGpio("up_switch")
		down_switch = radio.getSwitchGpio("down_switch")

		left_switch = radio.getSwitchGpio("left_switch")
		right_switch = radio.getSwitchGpio("right_switch")
		menu_switch = radio.getSwitchGpio("menu_switch")

		boardrevision = radio.getBoardRevision() 
		if boardrevision == 1:
			# For rev 1 boards with no inbuilt pull-up/down resistors
			# Wire the GPIO inputs to ground via a 10K resistor
			GPIO.setup(menu_switch, GPIO.IN)
			GPIO.setup(up_switch, GPIO.IN)
			GPIO.setup(down_switch, GPIO.IN)
			GPIO.setup(left_switch, GPIO.IN)
			GPIO.setup(right_switch, GPIO.IN)

		else:
			# For rev 2 boards with inbuilt pull-up/down resistors 
			# there is no need to physically wire the 10k resistors
			GPIO.setup(menu_switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
			GPIO.setup(up_switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
			GPIO.setup(down_switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
			GPIO.setup(left_switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
			GPIO.setup(right_switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

		# Initialise radio
		log.init('radio')
		signal.signal(signal.SIGTERM,signalHandler)

		progcall = str(sys.argv)
		log.message('Radio running pid ' + str(os.getpid()), log.INFO)
		log.message("Radio " +  progcall + " daemon version " + radio.getVersion(), log.INFO)
		log.message("GPIO version " + str(GPIO.VERSION), log.INFO)

		lcd.init(boardrevision)
		lcd.setWidth(20)
		lcd.line1("Radio version " + radio.getVersion())
		time.sleep(0.5)

		# Display daemon pid on the LCD
		message = "Radio pid " + str(os.getpid())
		lcd.line2(message)

		lcd.line3("Waiting for network")
		IPwait = 5	# Wait max 5s. for network
		while IPwait > 0:
			IPwait = IPwait - 1
			ipaddr = exec_cmd('hostname -I')
			if ipaddr is "":
				time.sleep(1)
			else:
				IPwait = 0

		lcd.line4("IP " + ipaddr)
		hostname = exec_cmd('hostname -s')
		log.message("IP " + ipaddr, log.INFO)

		lcd.line3("Starting MPD")
		radio.start()
		log.message("MPD started", log.INFO)
		time.sleep(0.5)

		if config.bright:	# LCD brightnes to high only if on in config file (Pecus)
			lcd.setBright(True)  # LCD backlight brightness to high (Pecus)

		mpd_version = radio.execMpcCommand("version")
		log.message(mpd_version, log.INFO)
		lcd.line3(mpd_version)
		lcd.line4("GPIO version " + str(GPIO.VERSION))
		time.sleep(2.0)
		 	
		reload(lcd,radio)
		#radio.play(get_stored_id(CurrentFile))
		#log.message("Current ID = " + str(radio.getCurrentID()), log.INFO)
		#lcd.line3("Radio Station " + str(radio.getCurrentID()))

		# Set up switch event processing
		GPIO.add_event_detect(menu_switch, GPIO.RISING, callback=switch_event, bouncetime=200)
		GPIO.add_event_detect(left_switch, GPIO.RISING, callback=switch_event, bouncetime=200)
		GPIO.add_event_detect(right_switch, GPIO.RISING, callback=switch_event, bouncetime=200)
		GPIO.add_event_detect(up_switch, GPIO.RISING, callback=switch_event, bouncetime=200)
		GPIO.add_event_detect(down_switch, GPIO.RISING, callback=switch_event, bouncetime=200)

		# Main processing loop
		count = 0 
		toggleScrolling = True	# Toggle scrolling between Line 2 and 3
		while True:

			# See if we have had an interrupt
			switch = radio.getSwitch()
			if switch > 0:
				get_switch_states(lcd,radio,rss)
				radio.setSwitch(0)

			display_mode = radio.getDisplayMode()
			lcd.setScrollSpeed(0.3) # Scroll speed normal
			dateFormat = radio.getDateFormat()
			todaysdate = strftime(dateFormat)
			ipaddr = exec_cmd('hostname -I')

			# Shutdown command issued
			if display_mode == radio.MODE_SHUTDOWN:
				displayShutdown(lcd)
				while True:
					time.sleep(1)

			elif ipaddr is "":
				lcd.line3("No IP network")

			elif display_mode == radio.MODE_TIME:
				if config.bright:	# LCD brightnes to high only if on in config file (Pecus)
					lcd.setBright(True)  # LCD backlight brightness to high (Pecus)
				if radio.getReload():
					log.message("Reload ", log.DEBUG)
					reload(lcd,radio)
					radio.setReload(False)

				input_source = radio.getSource()
				if input_source == radio.RADIO:
					msg = "r"
				elif input_source == radio.PLAYER:
					msg = "m"
				elif input_source == radio.PANDORA:
					msg = "p"
				msg = msg + ' ' + todaysdate  # extra space before time (Pecus)
				if radio.getStreaming():
					msg = msg + ' *' 
				lcd.line1(msg)
				display_current(lcd,radio,toggleScrolling)

			elif display_mode == radio.MODE_SEARCH:
				display_search(lcd,radio)

			elif display_mode == radio.MODE_SOURCE:
				display_source_select(lcd,radio)

			elif display_mode == radio.MODE_OPTIONS:
				display_options(lcd,radio)

			elif display_mode == radio.MODE_IP:
				displayInfo(lcd,ipaddr,mpd_version)

			elif display_mode == radio.MODE_RSS:
				msg = todaysdate + ' RSS'  # extra RSS mode info (Pecus)
				lcd.line1(msg)
				input_source = radio.getSource()
				current_id = radio.getCurrentID()
				if input_source == radio.RADIO or input_source == radio.PANDORA:
					station = radio.getRadioStation() 
					lcd.line2(station)
				else:
					lcd.line2(radio.getCurrentArtist())
				display_rss(lcd,rss)

			elif display_mode == radio.MODE_SLEEP:
				msg = '  ' + todaysdate  # extra 2 spaces before time (Pecus)
				lcd.line2(msg)  # in sleep mode time and date in second line of LCD (Pecus)
				display_sleep(lcd,radio)
				if config.rss:	# RSS in standby only if on in config file (Pecus)
					display_rss(lcd,rss)
				else:
					lcd.line3('')

			# Timer function
			checkTimer(radio)

			# Check state (pause or play)
			checkState(radio)
					
			# Alarm wakeup function
			if display_mode == radio.MODE_SLEEP and radio.alarmFired():
				log.message("Alarm fired", log.INFO)
				radio.unmute()
				displayWakeUpMessage(lcd)
				radio.setDisplayMode(radio.MODE_TIME)
					

			# Toggle line 2 & 3 scrolling
			if toggleScrolling:
				toggleScrolling = False
			else:
				toggleScrolling = True

			if display_mode == radio.MODE_SLEEP:
				if config.rss:
					time.sleep(0.1)
				else:
					time.sleep(1)
			else:
				time.sleep(0.1)
			
			# End of main processing loop

	def status(self):
		# Get the pid from the pidfile
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None

		if not pid:
			message = "radiod status: not running"
	    		log.message(message, log.INFO)
			print message 
		else:
			message = "radiod running pid " + str(pid)
	    		log.message(message, log.INFO)
			print message 
		return

# End of class overrides

# Scrolling LCD display interrupt routine
def interrupt():
	global lcd
	global radio
	global rss
	interrupt = False
	switch = radio.getSwitch()
	if switch > 0:
		interrupt = get_switch_states(lcd,radio,rss)
		radio.setSwitch(0)

	# Rapid display of track play status
	if radio.getDisplayMode() != radio.MODE_SLEEP:
		if radio.getSource() == radio.PLAYER or radio.getSource() == radio.PANDORA:
			if radio.volumeChanged():
				displayVolume(lcd,radio)
				time.sleep(0.5)
			else:
				displayProgress(lcd,radio)
		elif (radio.getTimer() and not interrupt) or radio.volumeChanged():
			displayVolume(lcd,radio)
			interrupt = checkTimer(radio)

		if not interrupt:
			interrupt = checkState(radio) or radio.getInterrupt()

		# sprawdzamy czy minal czas na potwierdzenie z Pandory i jesli tak to zerujemy flage potwierdzenia
		if radio.pandora_decision_time <= int(time.time()):
			radio.pandora_decision = radio.OK

	return interrupt

def no_interrupt(): 
	return False

# Call back routine called by switch events
def switch_event(switch):
	global radio
	radio.setSwitch(switch)
	return

# Check switch states
def get_switch_states(lcd,radio,rss):
	interrupt = False       # Interrupt display
	switch = radio.getSwitch()
	display_mode = radio.getDisplayMode()
	input_source = radio.getSource()
	option = radio.getOption()

	# Get switches configuration
	up_switch = radio.getSwitchGpio("up_switch")
	down_switch = radio.getSwitchGpio("down_switch")
	left_switch = radio.getSwitchGpio("left_switch")
	right_switch = radio.getSwitchGpio("right_switch")
	menu_switch = radio.getSwitchGpio("menu_switch")

	if switch == menu_switch:
		log.message("MENU switch", log.DEBUG)
		# Shutdown if menu button held for > 3 seconds
		MenuSwitch = GPIO.input(menu_switch)
		count = 15
		while MenuSwitch:
			time.sleep(0.2)
			MenuSwitch = GPIO.input(menu_switch)
			count = count - 1
			if count < 0:
				log.message("Shutdown", log.DEBUG)
				MenuSwitch = False
				radio.setDisplayMode(radio.MODE_SHUTDOWN)

		if display_mode == radio.MODE_SLEEP:
			# Send remote code (simulate IR remote key)
			udpSend('KEY_WAKEUP')
		else:
			if radio.muted():
				unmuteRadio(lcd,radio)
			# Send remote code (simulate IR remote key)
			udpSend('KEY_OK')

	elif switch == up_switch:
		log.message("UP switch display_mode " + str(display_mode), log.DEBUG)

		if  display_mode != radio.MODE_SLEEP:

			if display_mode == radio.MODE_TIME:
				# Send remote code (simulate IR remote key)
				udpSend('KEY_CHANNELUP')

			else:
				# Send remote code (simulate IR remote key)
				udpSend('KEY_UP')

		else:
			DisplayExitMessage(lcd)

	elif switch == down_switch:
		log.message("DOWN switch display_mode " + str(display_mode), log.DEBUG)

		if  display_mode != radio.MODE_SLEEP:

			if display_mode == radio.MODE_TIME:
				# Send remote code (simulate IR remote key)
				udpSend('KEY_CHANNELDOWN')

			else:
				# Send remote code (simulate IR remote key)
				udpSend('KEY_DOWN')

		else:
			DisplayExitMessage(lcd)

	elif switch == left_switch:
		log.message("LEFT switch" ,log.DEBUG)

		if  display_mode != radio.MODE_SLEEP:

			if display_mode == radio.MODE_TIME:
				if GPIO.input(right_switch):
					# Send remote code (simulate IR remote key)
					udpSend('KEY_MUTE')
				else:
					# Send remote code (simulate IR remote key)
					udpSend('KEY_VOLUMEDOWN')

			else:
				# Send remote code (simulate IR remote key)
				udpSend('KEY_LEFT')

		else:
			DisplayExitMessage(lcd)

	elif switch == right_switch:
		log.message("RIGHT switch" ,log.DEBUG)

		if  display_mode != radio.MODE_SLEEP:

			if display_mode == radio.MODE_TIME:
				if GPIO.input(left_switch):
					# Send remote code (simulate IR remote key)
					udpSend('KEY_MUTE')
				else:
					# Send remote code (simulate IR remote key)
					udpSend('KEY_VOLUMEUP')

			else:
				# Send remote code (simulate IR remote key)
				udpSend('KEY_RIGHT')

		else:
			DisplayExitMessage(lcd)

	return interrupt

# Sleep exit message
def DisplayExitMessage(lcd):
	lcd.line3("Press menu button to")
	lcd.line4("  exit sleep mode")
	time.sleep(1)
	lcd.line3("")
	lcd.line4("")
	return

# Update music library
def update_library(lcd,radio):
	log.message("Updating library", log.INFO)
	lcd.line1("Updating library")
	lcd.line2("Please wait")
	radio.updateLibrary()
	return

# Reload if new source selected (RADIO or PLAYER)
def reload(lcd,radio):
	lcd.line1("Loading:")
	lcd.line3("Wait...")
	lcd.line4("")

	source = radio.getSource()
	if source == radio.RADIO:
		lcd.line2("Radio Stations")
		dirList=os.listdir(PlaylistsDirectory)
		for fname in dirList:
			if os.path.isfile(fname):
				continue
			log.message("Loading " + fname, log.DEBUG)
			lcd.line2(fname)
			time.sleep(0.1)
		radio.loadStations()

	elif source == radio.PLAYER:
		lcd.line2("Media library")
		radio.loadMedia()
		current = radio.execMpcCommand("current")
		if len(current) < 1 or radio.getUpdateLibrary() or config.media_update: # If uptade flags set, update library on source switch (Pecus)
			update_library(lcd,radio)

	elif source == radio.PANDORA:
		lcd.line2("Pandora radio")
		radio.loadPandora()

	return

# Display the RSS feed
def display_rss(lcd,rss):
	rss_line = rss.getFeed()
	lcd.setScrollSpeed(0.2) # Scroll RSS a bit faster
	lcd.scroll3(rss_line,interrupt)
	return

# Display the currently playing station or track
def display_current(lcd,radio,toggleScrolling):
	station = radio.getRadioStation()
	title = radio.getCurrentTitle()
	current_id = radio.getCurrentID()
	source = radio.getSource()

	# Display progress of the currently playing track
	if radio.muted():
		displayVolume(lcd,radio)
	else:
		if source == radio.PLAYER or source == radio.PANDORA:
			displayProgress(lcd,radio) 
		else:
			displayVolume(lcd,radio) 

	if source == radio.RADIO:
		if len(title) < 1:
			bitrate = radio.getBitRate()
			if bitrate > 0:
				title = "Station " + str(current_id) + ' ' + str(bitrate) +'k'
		if current_id <= 0:
			lcd.line2("No stations found")
		else:
			if toggleScrolling:
				lcd.line3(title)
				lcd.scroll2(station, interrupt)
			else:
				lcd.line2(station)
	elif source == radio.PANDORA:
		if toggleScrolling:
			lcd.line3(title)
			lcd.scroll2(station, interrupt)
		else:
			lcd.line2(station)
	else:
		index = radio.getSearchIndex()
		playlist = radio.getPlayList()
		current_artist = radio.getCurrentArtist()
		lcd.line2(current_artist)

	# Send metadata to icecast server
	if radio.streaming:
		if radio.streammetadata != title:
			radio.streammetadata = title
			metadataFormatted = radio.streammetadata.replace(" ","+") #add "+" instead of " " for icecast2
			requestToSend = ("http://localhost:8001/admin/metadata?mount=/mpd&mode=updinfo&song=") +(metadataFormatted)
			r = requests.get((requestToSend), auth=("admin","mympd"))

	# Display stream error 
	if radio.gotError():
		errorStr = radio.getErrorString()
		lcd.scroll3(errorStr,interrupt)
		radio.clearError()
	else:
		leng = len(title)
		if leng > 20:
			if toggleScrolling:
				lcd.line3(title)
			else:
				lcd.scroll3(title[0:160],interrupt)
		else:
			lcd.line3(title)

	return

# Display if in sleep
def display_sleep(lcd,radio):
	message = ''  # I don't like text "Sleep mode" in sleep mode (Pecus)
	lcd.setBright(False)  # LCD backlight brightness to low (Pecus)
	lcd.line1('')  # time is now in second line, therefore we clean first line (Pecus)
	if radio.alarmActive():
		message = "Alarm " + radio.getAlarmTime()
	lcd.line4(message)
	return

# Get the last ID stored in /var/lib/radiod
def get_stored_id(current_file):
	current_id = 5
	if os.path.isfile(current_file):
		current_id = int(readFromFile(current_file) ) # (Pecus)
	return current_id

# Execute system command
def exec_cmd(cmd):
	p = os.popen(cmd)
	result = p.readline().rstrip('\n')
	return result

# Read text line from file (Pecus)
def readFromFile(fname): # (Pecus)
	file = open(fname, "r") # (Pecus)
	text = file.readline() # (Pecus)
	file.close() # (Pecus)
	return text # (Pecus)

# Get list of tracks or stations
def get_mpc_list(cmd):
	list = []
	line = ""
	p = os.popen("/usr/bin/mpc " + cmd)
	while True:
		line =  p.readline().strip('\n')
		if line.__len__() < 1:
			break
		list.append(line)

	return list

# Source selection display
def display_source_select(lcd,radio):

	lcd.line1("Input Source:")
	source = radio.getSource()
	if source == radio.RADIO:
		lcd.line2("Internet Radio")

	elif source == radio.PLAYER:
		lcd.line2("Music Player")

	elif source == radio.PANDORA:
		lcd.line2("Pandora Radio")

	return

# Display search (Station or Track)
def display_search(lcd,radio):
	index = radio.getSearchIndex()
	source = radio.getSource()
	current_id = radio.getCurrentID()

	if source == radio.PLAYER:
		lcd.line1("Search:" + str(index + 1))
		current_artist = radio.getArtistName(index)
		lcd.scroll2(current_artist[0:160],interrupt) 
		lcd.scroll3(radio.getTrackNameByIndex(index),interrupt) 
		lcd.line4(radio.getProgress())
	elif source == radio.PANDORA:
		lcd.line1("Search:" + str(radio.pandora_search_index + 1))
		current_station = radio.getPandoraStationName(radio.pandora_search_index)
		lcd.line3("Current station:" + str(radio.current_pandora_id))
		lcd.scroll2(current_station[0:160],interrupt) 
		lcd.line4(radio.getProgress())
		pass
	else:
		lcd.line1("Search:" + str(index + 1))
		current_station = radio.getStationName(index)
		lcd.line3("Current station:" + str(radio.getCurrentID()))
		lcd.scroll2(current_station[0:160],interrupt) 
	return

# Unmute radio and get stored volume
def unmuteRadio(lcd,radio):
	radio.unmute()
	volume = radio.getVolume()
	lcd.line4("Volume " + str(VolumeToDisplay(volume)))
#	radio.setDisplayMode(radio.MODE_TIME)
	return

# Options menu
def display_options(lcd,radio):
	option = radio.getOption()

	if option != radio.TIMER and option != radio.ALARM \
			and option != radio.ALARMSETHOURS and option != radio.ALARMSETMINS :
		lcd.line1("Menu selection:")

	if option == radio.RANDOM:
		if radio.getRandom():
			lcd.line2("Random on")
		else:
			lcd.line2("Random off")

	elif option == radio.CONSUME:
		if radio.getConsume():
			lcd.line2("Consume on")
		else:
			lcd.line2("Consume off")

	elif option == radio.REPEAT:
		if radio.getRepeat():
			lcd.line2("Repeat on")
		else:
			lcd.line2("Repeat off")

	elif option == radio.TIMER:
		lcd.line1("Set timer function:")
		if radio.getTimer():
			lcd.line2("Timer " + radio.getTimerString())
		else:
			lcd.line2("Timer off")

	elif option == radio.ALARM:
		alarmString = "off"
		lcd.line1("Set alarm function:")
		alarmType = radio.getAlarmType()

		if alarmType == radio.ALARM_ON:
			alarmString = "on"
		elif alarmType == radio.ALARM_REPEAT:
			alarmString = "repeat"
		elif alarmType == radio.ALARM_WEEKDAYS:
			alarmString = "weekdays only"
		lcd.line2("Alarm " + alarmString)

	elif option == radio.ALARMSETHOURS:
		lcd.line1("Set alarm time:")
		lcd.line2("Alarm " + radio.getAlarmTime() + " hours")

	elif option == radio.ALARMSETMINS:
		lcd.line1("Set alarm time:")
		lcd.line2("Alarm " + radio.getAlarmTime() + " mins")

	elif option == radio.STREAMING:
		if radio.getStreaming():
			lcd.line2("Streaming on")
		else:
			lcd.line2("Streaming off")

	elif option == radio.RELOADLIB:
		if radio.getUpdateLibrary():
			lcd.line2("Update playlist: Yes")
		else:
			lcd.line2("Update playlist: No")

	if  radio.getSource() == radio.PLAYER or radio.getSource() == radio.PANDORA:
		lcd.line4(radio.getProgress())

	return

# Display volume and timer
def displayVolume(lcd,radio):
	if radio.muted():
		msg = "Sound muted"
	else:
		msg = "Volume " + str(VolumeToDisplay(radio.getVolume()))
	if radio.getTimer():
		msg = msg + " " + radio.getTimerString()
	if radio.alarmActive():
		msg = msg + ' ' + radio.getAlarmTime()
	lcd.line4(msg)
	return

# Display progress and timer
def displayProgress(lcd,radio):
	if radio.muted():
		msg = "Sound muted"
	else:
		msg = str(radio.getProgress())
	if radio.getTimer():
		msg = msg + " " + radio.getTimerString()
	if radio.alarmActive():
		msg = msg + ' ' + radio.getAlarmTime()
	if radio.getSource() == radio.PANDORA and radio.pandora_decision != radio.OK:
		# jesli czekamy na potwierdzenie decyzji w Pandorze to zamiast progresu wyswietlamy rodzaj decyzji
		if radio.pandora_decision == radio.UP:
			msg = "Like this track. OK?"
		elif radio.pandora_decision == radio.DOWN:
			msg = "Ban this track.  OK?"
		elif radio.pandora_decision == radio.LEFT:
			msg = "Tired this track.OK?"
	lcd.line4(msg)
	return

# Display wake up message
def displayWakeUpMessage(lcd):
	message = 'Good day'
	t = datetime.datetime.now()
	if t.hour >= 0 and t.hour < 12: 
		message = 'Good morning'
	if t.hour >= 12 and t.hour < 18: 
		message = 'Good afternoon'
	if t.hour >= 16 and t.hour <= 23: 
		message = 'Good evening'
	lcd.line4(message)
	time.sleep(3)
	return

def displayShutdown(lcd):
	lcd.setBright(False)  # LCD backlight brightness to low (Pecus)
	lcd.line1("   Stopping radio")
	radio.execCommand("service mpd stop")
	radio.pandora_stop()
	lcd.line2(" ")
	lcd.line3(" ")
	lcd.line4(" ")
	radio.execCommand("shutdown -h now")
	lcd.line2("   Shutdown issued")
	time.sleep(3)
	lcd.line1("   Radio stopped")
	lcd.line2("  Power off radio")
	return

def displayInfo(lcd,ipaddr,mpd_version):
	lcd.line2("Radio version " + radio.getVersion())
	lcd.line3(mpd_version)
	lcd.line4("GPIO version " + GPIO.VERSION)
	if ipaddr is "":
		lcd.line3("No IP network")
	else:
		lcd.scroll1("IP "+ ipaddr,interrupt)
	return

def VolumeToDisplay(volume):
	volume = (volume - config.getVolumeMin()) * 100
	tym = (config.getVolumeMax() - config.getVolumeMin())
	volume = volume / tym
	return volume

# Check Timer fired
def checkTimer(radio):
	interrupt = False
	if radio.fireTimer():
		log.message("Timer fired", log.INFO)
		radio.mute()
		if radio.getSource() == radio.PANDORA:	# Jesli gra pandora to nie pauzujemy (mutujemy) tylko stopujemy
			radio.pandora_stop()
		radio.setDisplayMode(radio.MODE_SLEEP)
		interrupt = True
	return interrupt

# Check state (pause or play)
# If external client such as mpc or MPDroid issue a pause or play command 
# Returns paused True if paused
def checkState(radio):
	paused = False
	display_mode = radio.getDisplayMode()
	state = radio.getState()
	radio.getVolume()

	if state == 'pause':
		paused = True
		if not radio.muted():
			if radio.alarmActive() and not radio.getTimer():
				radio.setDisplayMode(radio.MODE_SLEEP)
			radio.mute()
	elif state == 'play':
		if radio.muted():
			unmuteRadio(lcd,radio)
			radio.setDisplayMode(radio.MODE_TIME)
	return paused

# Send button data to radio program
def udpSend(button):
	udpport = config.getRemoteUdpPort()
	udphost = config.getRemoteUdpHost()
	data = ''
	log.message("radio4.udpSend " + button, log.DEBUG)
	
	try:
		clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		clientsocket.settimeout(3)
		clientsocket.sendto(button, (udphost, udpport))
		data = clientsocket.recv(100).strip()

	except socket.error, e:
		err = e.args[0]
		if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
			log.message("radio4.udpSend no data" + e, log.ERROR)
		else:
			# Errors such as timeout
			log.message("radio4.udpSend " + str(e), log.ERROR)

	if len(data) > 0:
		log.message("radio4.udpSend server sent: " + data, log.DEBUG)
	return data


### Main routine ###
if __name__ == "__main__":
	daemon = MyDaemon('/var/run/radiod.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			os.system("service mpd stop")
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'status' == sys.argv[1]:
			daemon.status()
		elif 'nodaemon' == sys.argv[1]:
			daemon.nodaemon()
		elif 'version' == sys.argv[1]:
			print "Version " + radio.getVersion()
		else:
			print "Unknown command: " + sys.argv[1]
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart|status|version|nodaemon" % sys.argv[0]
		sys.exit(2)

# End of script 
