#!/bin/bash
find "$1" -perm -u=s -exec ls -la {} \; 2>/dev/null
