#!/bin/bash
sudo nmap -sM -vv -p http,ssh,telnet,ftp,https $1
