#!/bin/bash
[ -z "$1" ] && { echo "Usage: $0 <password>"; exit 1; }
echo -n "$1" | sha1sum | awk '{print $1}' > 0_hash.txt
