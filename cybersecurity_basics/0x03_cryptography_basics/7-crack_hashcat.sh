#!/bin/bash
hashcat -m 0 -a 0 -O -w 1 hash.txt /usr/share/wordlists/rockyou.txt
