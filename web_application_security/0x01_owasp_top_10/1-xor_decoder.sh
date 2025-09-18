#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 {xor}<base64_string>"
    exit 1
fi

input="$1"
prefix="{xor}"

if [[ "$input" != "$prefix"* ]]; then
    echo "Error: Input does not start with '{xor}'" >&2
    exit 1
fi

base64_str="${input:${#prefix}}"

# Check if base64 string is valid
if ! echo -n "$base64_str" | base64 -d > /dev/null 2>&1; then
    echo "Error: Invalid base64 string" >&2
    exit 1
fi

# Process each byte after base64 decoding
echo -n "$base64_str" | base64 -d | od -t u1 -An -v | tr -s ' ' '\n' | grep -v '^$' | while read byte; do
    xor_val=$((byte ^ 0x5F))
    printf "\\$(printf "%03o" "$xor_val")"
done
