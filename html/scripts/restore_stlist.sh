# Restore station list from file

# Only if 1 params
if [ $# = 1 ]; then
	# Get parameter from commandline
	
	# "unpack" or "apply"
	OPTION=$1

	# Unpack or apply
	if [ ${OPTION} = "unpack" ]; then
		# prepare temp folder
		rm -r /tmp/radiod/config
		mkdir /tmp/radiod/config
		# Unpack configuration
		cd /tmp/radiod/config
		tar -zxf /tmp/piradio.stl
		# remove station list backup file
		rm /tmp/piradio.stl
	elif [ ${OPTION} = "apply" ]; then
		# PiRadio statiolist file
		cp /tmp/radiod/config/radiod/stationlist /var/lib/radiod/
		cp /tmp/radiod/config/radiod/current_station /var/lib/radiod/
		# MPD playlists
		rm /var/lib/mpd/playlists/*
		cp /tmp/radiod/config/playlists/* /var/lib/mpd/playlists/
		# clear temp
		rm -r /tmp/radiod/config
	fi
fi
