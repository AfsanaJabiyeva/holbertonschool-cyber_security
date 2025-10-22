#!/bin/bash
hashcat -m 0 -a 1 hash.txt wordlist1.txt wordlist2.txt
