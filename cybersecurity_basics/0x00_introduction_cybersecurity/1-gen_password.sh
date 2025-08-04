#!/bin/bash
echo $(tr -dc [:alnum:] < /dev/urandom | head -c $1)

