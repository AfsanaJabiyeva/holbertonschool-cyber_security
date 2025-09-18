#!/bin/bash
hash=$1
hash="${hash#\{xor\}}"
decoded=$(echo "$hash" | base64 -d 2>/dev/null)
output=""
for ((i=0; i<${#decoded}; i++)); do
    char=$(printf "%d" "'${decoded:$i:1}")
    xor=$((char ^ 0x5A))
    output+=$(printf "\\x$(printf %x $xor)")
done

echo -n "$output"
