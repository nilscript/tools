#!/bin/sh

command="cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1"

if [ "$1" = "-h" ] || [ "$1" = "--help" ]
then
    printf "\e[1m[Usage]\e[0m:\n"
    printf "  %s\n" "$(basename $0)"
    printf "\n"
    printf "  Generates a psuedo random string with this command:\n"
    printf "  %s\n" "$command"

    exit 0
fi

eval "$command"
