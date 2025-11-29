#!/bin/bash
awk '{print $2}' logs.txt | sort | uniq -c | sort -nr | head -1
