# Copy new version of ir config file (overwrite old)
cp --preserve=timestamp -R /usr/share/radio/hardware/ir/lircrc /etc/lirc/

# Set up loopback audio module
modprobe snd-aloop

# Install darkice for encoding said audio stream into mp3
apt-get -y install darkice
