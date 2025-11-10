#!/bin/bash
sudo nmap -sX -open -p 440-450 --packet-trace --reason -v $1
