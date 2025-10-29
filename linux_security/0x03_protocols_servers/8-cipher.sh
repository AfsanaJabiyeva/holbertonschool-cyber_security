#!/bin/bash
nmap --script ssl-enum-ciphers -p 80 "$1"
