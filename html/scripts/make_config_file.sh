# Backup current configuration

# prepare temp folder
rm -r /tmp/radiod/config
mkdir /tmp/radiod/config

# Version
cp /usr/share/radio/version /tmp/radiod/config/

# Boot config
cp /boot/config.txt /tmp/radiod/config/

# MPD config
cp /etc/mpd.conf /tmp/radiod/config/

# SoundCard prioryty
cp /lib/modprobe.d/aliases.conf /tmp/radiod/config/

# IR Remote config
cp /etc/lirc/lircd.conf /tmp/radiod/config/

# PiRadio main config
cp /etc/radiod.conf /tmp/radiod/config/

# PiRadio config files
mkdir /tmp/radiod/config/radiod/
cp /var/lib/radiod/* /tmp/radiod/config/radiod/

# MPD playlists
mkdir /tmp/radiod/config/playlists/
cp /var/lib/mpd/playlists/* /tmp/radiod/config/playlists/

# Pianobar setup
mkdir /tmp/radiod/config/pianobar/
cp /home/pi/.config/pianobar/* /tmp/radiod/config/pianobar/

# Make ready for download file
cd /tmp/radiod/config
tar -zcf /home/pi/radio/html/piradio.set *

# clear temp
rm -r /tmp/radiod/config
