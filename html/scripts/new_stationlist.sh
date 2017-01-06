# Create new stationlist form a /var/lib/radiod/stationlist_new file
chmod -R 0777 /var/lib/radiod/*

# Check for new stationlist file
if [ -f "/var/lib/radiod/stationlist_new" ]
then
	# Remove old copy of stationlist file
	rm -r /var/lib/radiod/stationlist_old
	# Rename current stationlist file - make old copy
	mv /var/lib/radiod/stationlist /var/lib/radiod/stationlist_old
	# Rename new stationlist file - make current stationlist
	mv /var/lib/radiod/stationlist_new /var/lib/radiod/stationlist
	# Call python script to make playlist from stationlist file
	python /usr/share/radio/create_m3u.py --delete_old
	echo "$file found."
else
	echo "stationlist_new not found."
fi

# Reastart PiRadio
service radiod restart
