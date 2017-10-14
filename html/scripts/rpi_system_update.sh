# stop radio service
service radiod stop

# call clear caches script first
/usr/share/radio/html/scripts/clear_caches.sh

# get actual packages list
apt-get update

# update all installed system packages and reboot
apt-get -y dist-upgrade
reboot
