#!/bin/sh

# Take a quick note of something

file=""

if [ -n "$1" ] 
then 
	file="$1"
else
	file="note"
fi

vim "$file-$(date +%y-%m-%d).md"

