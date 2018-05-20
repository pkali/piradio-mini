# Backup current station list to file

# prepare temp folder
rm -r /tmp/radiod/config
mkdir /tmp/radiod/config

# Version
cp /usr/share/radio/version /tmp/radiod/config/

# PiRadio stationlist file
mkdir /tmp/radiod/config/radiod/
cp /var/lib/radiod/stationlist /tmp/radiod/config/radiod/

# MPD playlists
mkdir /tmp/radiod/config/playlists/
cp /var/lib/mpd/playlists/* /tmp/radiod/config/playlists/

# Make ready for download file
cd /tmp/radiod/config
tar -zcf /home/pi/radio/html/piradio.stl *

# clear temp
rm -r /tmp/radiod/config
