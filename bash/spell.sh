#!/usr/bin/env bash

if ! [ -f "$HOME/.dmenurc" ]
then
	cp /usr/share/dmenu/dmenurs "$HOME"/.dmenurc
fi

dict="american-english"

cd "/usr/share/dict/" || cd "/var/lib/dict" || (
	echo "Can't find installed dictionaries"
	exit 1
)

if [ -n "$1" ]
then

	if [ "$1" = "--help" ]
	then
		echo "Usage: $0 [ -d | \"dict_path\" ]"

	elif [ "$1" = "-d" ]
	then
		dict="$(find . -type f | dmenu -l 30)"	

	else
		dict="$1"

	fi
	
fi

dmenu "$DMENU_OPTIONS" < "$dict"
