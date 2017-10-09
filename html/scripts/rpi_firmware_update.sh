# stop radio service
service radiod stop

# call clear caches script first
/usr/share/radio/html/scripts/clear_caches.sh

# get actual packages list
apt-get update

# install firmware update app
apt-get -y install rpi-update

# firmware update and reboot
rpi-update
reboot
