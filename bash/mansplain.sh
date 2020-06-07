#!/usr/bin/env sh


if [ "$1" = "-h" ] || [ "$1" = "--help" ]
then
    printf "\e[1m[Usage]\e[0m: %s\n" "$0"
    printf "A copy of Luke Smith oneliner pipe from one of his videos: https://youtu.be/8E8sUNHdzG8 \n"
    printf "Looks up manuals with dmenu.\n"
    printf "No longer opens them in pdf due to pdfs being inferior than man itself.\n"
    exit 0
fi

man -k . | dmenu -l 30 | awk '{print $1}' | xargs -r man

