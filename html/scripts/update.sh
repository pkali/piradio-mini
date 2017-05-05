# Copy new version of ir config file (overwrite old)
cp --preserve=timestamp -R /usr/share/radio/hardware/ir/lircrc /etc/lirc/

# Set up loopback audio module
modprobe -f snd-aloop

# Install darkice for encoding said audio stream into mp3
apt-get -y install darkice

# Install python library to send metadata to icecast server
 apt-get -y install python-requests
 
# Set up new audio config files
cp /usr/share/radio/hardware/audio/asoundrc /home/pi/.asoundrc
cp /usr/share/radio/hardware/audio/mpd.conf /etc/mpd.conf
cp /usr/share/radio/hardware/audio/darkice.cfg /etc/darkice.cfg
cp /usr/share/radio/hardware/audio/libao.conf /etc/libao.conf
cp /usr/share/radio/hardware/audio/darkice /etc/init.d/darkice
cp /usr/share/radio/hardware/audio/internal.conf /lib/modprobe.d/aliases.conf
