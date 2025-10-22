#!/bin/bash
if ["$USER"="user2"]; then find "$1" -type f -exec chown user3 {};\; fi
