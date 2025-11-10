#!/bin/bash
sudo nmap -sX -p 440-450 --packet-trace --reason -v $1
