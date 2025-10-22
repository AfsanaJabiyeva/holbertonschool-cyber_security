#!/bin/bash
find "$1" -type f -mtime -1 -perm -u=s -o -perm -2000 -exec ls -la {}\;
