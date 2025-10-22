#!/bin/bash
find "$1" -mtime -1 -perm -u=s -2000
