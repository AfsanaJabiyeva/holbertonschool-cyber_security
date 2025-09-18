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
decoded=$(base64 -d <<< "$base64_str" 2>/dev/null)

if [ $? -ne 0 ]; then
    echo "Error: Invalid base64 string" >&2
    exit 1
fi

output=""
for (( i=0; i<${#decoded}; i++ )); do
    char="${decoded:$i:1}"
    byte_val=$(printf "%d" "'$char")
    xor_val=$((byte_val ^ 0x5F))
    output+=$(printf "\\$(printf "%03o" "$xor_val")")
done

echo -n "$output"
