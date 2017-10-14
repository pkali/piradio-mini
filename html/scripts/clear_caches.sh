# Remove firmware update backup
rm -r /boot.bak

# Remove backups
rm /var/backups/*.gz

# Remove caches
rm /var/cache/debconf/*.dat-old
apt-get clean

# Remove old logs
rm /var/log/*.gz
rm /var/log/apache2/*.gz
rm /var/log/apt/*.gz
rm /var/log/icecast2/*.gz
rm /var/log/mpd/*.gz
rm /var/log/samba/*.*
