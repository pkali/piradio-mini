# Restore configuration from file

# Only if 1 params
if [ $# = 1 ]; then
	# Get parameter from commandline
	
	# "unpack" or "apply"
	OPTION=$1

	# Unpack or apply config
	if [ ${OPTION} = "unpack" ]; then
		# prepare temp folder
		rm -r /tmp/radiod/config
		mkdir /tmp/radiod/config
		# Unpack configuration
		cd /tmp/radiod/config
		tar -zxf /tmp/piradio.set
		# remove donfig file
		rm /tmp/piradio.set
	elif [ ${OPTION} = "apply" ]; then
		# Boot config
		cp /tmp/radiod/config/config.txt /boot/
		# MPD config
		cp /tmp/radiod/config/mpd.conf /etc/
		# SoundCard prioryty
		cp /tmp/radiod/config/aliases.conf /lib/modprobe.d/
		# IR Remote config
		cp /tmp/radiod/config/lircd.conf /etc/lirc/
		# PiRadio main config
		cp /tmp/radiod/config/radiod.conf /etc/
		# PiRadio config files
		cp /tmp/radiod/config/radiod/* /var/lib/radiod/
		# MPD playlists
		rm /var/lib/mpd/playlists/*
		cp /tmp/radiod/config/playlists/* /var/lib/mpd/playlists/
		# Pianobar setup
		cp /tmp/radiod/config/pianobar/* /home/pi/.config/pianobar/
		# clear temp
		rm -r /tmp/radiod/config
	fi
fi
