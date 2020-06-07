#!/usr/bin/env bash

if [ "$1" = "-h" ] || [ "$1" = "--help" ]
then
	printf "Usage: %s\n" "$0"
	printf "Color escapes are %s\n" "\e[\${value};...;\${value}m"
	printf "Values 30..37 are \e[33mforeground colors\e[m\n"
	printf "Values 40..47 are \e[43mbackground colors\e[m\n"
	printf "Value 1 gives a \e[1mbold-faced look\e[m\n"
	exit 0
fi

# foreground colors
for fgc in {30..37}; do

	# background colors
	for bgc in {40..47}; do
		fgc=${fgc#37} # white
		bgc=${bgc#40} # black

		vals="${fgc:+$fgc;}${bgc}"
		vals=${vals%%;}

		seq0="${vals:+\e[${vals}m}"
		printf "  %-9s" "${seq0:-(default)}"
		printf " %sTEXT\e[m" "${seq0}"
		printf " \e[%s1mBOLD\e[m" "${vals:+${vals+$vals;}}"
	done
	printf "\n"
done
