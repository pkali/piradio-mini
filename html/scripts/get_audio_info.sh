aplay -l | grep "card 0" -m 1
amixer -c0 scontrols | grep "Simple" -m 1
aplay -l | grep "card 1" -m 1
amixer -c1 scontrols | grep "Simple" -m 1

