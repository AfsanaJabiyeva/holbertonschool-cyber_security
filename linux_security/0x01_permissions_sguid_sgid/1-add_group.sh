#!/bin/bash
addgroup "$1"
chmod 674 "$2"
chown :"$1" "$2"
