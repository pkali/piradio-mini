#!/bin/bash

# Files to modify

BOOTCONFIG=/boot/config.txt
MPDCONFIG=/etc/mpd.conf
CARDPRIORYTY=/lib/modprobe.d/aliases.conf

INTERNALFIRST=/usr/share/radio/hardware/audio/internal.conf
USBFIRST=/usr/share/radio/hardware/audio/usb.conf

# Only if 3 params
if [ $# = 3 ]; then
	# Get parameters from commandline
	
	# "internal or "usb"
	CARD=$1
	# Mixer name for volume control
	MIXER=$2
	# PWM mode 1 - standard , 2 - high quality
	PWM=$3

	# Set prioryty of audio device
	if [ ${CARD} = "internal" ]; then
		cp ${INTERNALFIRST} ${CARDPRIORYTY}
	elif [ ${CARD} = "usb" ]; then
		cp ${USBFIRST} ${CARDPRIORYTY}
	fi

	# Set PWM mode
	sed -i "s/audio_pwm_mode.*/audio_pwm_mode=${PWM}/" ${BOOTCONFIG}

	# Set mixer name
	sed -i "s/^[ \t]*mixer_control.*/\tmixer_control\t\"${MIXER}\"/" ${MPDCONFIG}
	
	reboot
fi
