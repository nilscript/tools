#!/bin/bash

if [ "$1" = "--help" ]; then
	printf "This command is equivalent to 'nohup <command> & > /dev/null'\n"
	printf "Anything after \"%s\" is considered part of <command>\n" "$0"
	printf "Remember to escape shell (like && and ||) sequenses with \"\"\n"
fi

nohup "${@:1}" > /dev/null
