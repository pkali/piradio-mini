# Download actual master from github
wget --output-document=/home/pi/piradionew.zip https://github.com/Pecusx/piradio-mini/archive/master.zip

# Unzip to temp dir: /usr/share/piradio-mini-master
rm -r /usr/share/piradio-mini-master
unzip /home/pi/piradionew.zip -d /usr/share/
