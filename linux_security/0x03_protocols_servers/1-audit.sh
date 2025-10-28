#!/bin/bash
grep -E -v "^#|^$" /etc/ssh/sshd_config
