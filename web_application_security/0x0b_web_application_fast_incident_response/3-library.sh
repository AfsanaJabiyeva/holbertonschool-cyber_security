#!/bin/bash
awk '{print $12}' logs.txt |tr -d '"'| sort | uniq -c | sort -nr | head -1 | awk '{print $2}'
