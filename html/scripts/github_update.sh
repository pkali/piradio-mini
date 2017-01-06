# Actual master from github downloaded and unpacked by github_download.sh (update.php)
# Backup actual files
tar -cvzf /home/pi/backup.tar /usr/share/radio/

# Copy new version of files (overwrite old)
cp --preserve=timestamp -R /usr/share/piradio-mini-master/* /usr/share/radio/
chmod -R 0777 /usr/share/radio/*

# Remove temp dir: /usr/share/piradio-mini-master
rm -r /usr/share/piradio-mini-master

# Remove github file
rm /home/pi/piradionew.zip

# Check for additional update script
if [ -f "/usr/share/radio/html/scripts/update.sh" ]
then
	# Call update script
	/usr/share/radio/html/scripts/update.sh
	# Remove update script
	rm /usr/share/radio/html/scripts/update.sh
fi

# Reboot after update
reboot
