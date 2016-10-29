# Download actual master from github
wget --output-document=/home/pi/piradionew.zip https://github.com/pkali/piradio-mini/archive/master.zip

# Unzip to temp dir: /usr/share/piradio-mini-master
rm -r /usr/share/piradio-mini-master
unzip /home/pi/piradionew.zip -d /usr/share/

# Backup actual files
tar -cvzf /home/pi/backup.tar /usr/share/radio/

# Copy new version of files (overwrite old)
cp -R /usr/share/piradio-mini-master/* /usr/share/radio/
chmod -R 0777 /usr/share/radio/*

# Remove temp dir: /usr/share/piradio-mini-master
rm -r /usr/share/piradio-mini-master

# Reboot after update
reboot
