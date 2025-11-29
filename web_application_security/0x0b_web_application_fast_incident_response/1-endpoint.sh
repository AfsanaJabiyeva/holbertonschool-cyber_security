#!/bin/bash
awk '{print $6}' | sort | uniq -c | sort -nr | head -1 | awk '{print $2}'
