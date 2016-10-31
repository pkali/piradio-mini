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

# Reboot after update
reboot
