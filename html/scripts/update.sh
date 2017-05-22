# Set up new stream encoder config files
cp /usr/share/radio/hardware/audio/darkice.cfg /etc/darkice.cfg

# install MPD 0.19.12 from package
cp /etc/mpd.conf /usr/share/radio/mpd.conf
dpkg --force-all -i /usr/share/radio/software/mpd_0.19.12-1~bpo8+1_armhf.deb
cp /usr/share/radio/mpd.conf /etc/mpd.conf
rm /usr/share/radio/mpd.conf
