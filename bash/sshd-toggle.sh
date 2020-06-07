#!/usr/bin/env bash

case "$1" in

	"-h" | "--help")
		printf "\e[1m[Usage]\e[0m: %s <start | stop>\n" "$0"
 		printf "start will start sshd\n"
		printf "stop will stop sshd\n"
 		printf "'nothing' will toggle sshd on or off\n"
		exit 0

		;;

	start)	
		sudo systemctl start sshd
		;;

	stop)
		sudo systemctl stop sshd
		;;

	"")
		if [ "$(systemctl is-active sshd)" = "active" ];
		then
			$0 stop
		else
			$0 start
		fi
		exit 0

esac

printf  "sshd: %s\n" "$(sudo systemctl is-active sshd)"
