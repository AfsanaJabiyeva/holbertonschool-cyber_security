#!/bin/bash
ps aux | grep "^$root" | grep -vE " 0.0"
