#!/usr/bin/env python3
import sys
import os

# Step 1: Check you gave exactly 3 arguments
# Example: python3 script.py 12345 Holberton maroua
if len(sys.argv) != 4:
    print("Usage: read_write_heap.py <pid> <search> <replace>", file=sys.stderr)
    sys.exit(1)

pid = int(sys.argv[1])              # the PID of ./main
search = sys.argv[2]                # "Holberton"
replace = sys.argv[3]               # "maroua"

# Convert to bytes (because memory is raw bytes, not Python strings)
search_bytes = search.encode('ascii')
replace_bytes = replace.encode('ascii')

# Safety: don’t allow replacement longer than original → would be real overflow
if len(replace_bytes) > len(search_bytes):
    print("Error: replacement string cannot be longer than search string", file=sys.stderr)
    sys.exit(1)

# Step 2: Find where the heap is
maps_path = f"/proc/{pid}/maps"     # This file lists all memory regions
heap_start = None
heap_end = None

with open(maps_path) as f:
    for line in f:
        if '[heap]' in line:                    # This is the exact line we want
            addr = line.split()[0]              # something like "55d2f7b34000-55d2f7b55000"
            heap_start = int(addr.split('-')[0], 16)   # convert hex string → number
            heap_end   = int(addr.split('-')[1], 16)
            print(f"[+] Found heap: {heap_start:#x} - {heap_end:#x}")
            break

if not heap_start:
    print("[-] No heap found. Is the process running?")
    sys.exit(1)

# Step 3: Open the raw memory of the process
mem_path = f"/proc/{pid}/mem"
if not os.access(mem_path, os.R_OK | os.W_OK):
    print("[-] Cannot open /proc/<pid>/mem → run with sudo!")
    sys.exit(1)

found = False
with open(mem_path, 'rb+') as mem:          # rb+ = read + write binary
    # Go to the beginning of the heap
    mem.seek(heap_start)

    # Read the entire heap into Python memory (usually tiny)
    heap_data = mem.read(heap_end - heap_start)

    # Search inside the heap data
    pos = 0
    while True:
        idx = heap_data.find(search_bytes, pos)
        if idx == -1:
            break                                   # not found anymore

        address = heap_start + idx                  # real address in the process
        print(f"[+] Found '{search}' at 0x{address:x}")

        # Write the new string + padding zeros
        new_data = replace_bytes + b'\x00' * (len(search_bytes) - len(replace_bytes))
        mem.seek(address)
        mem.write(new_data)
        print(f"    → Replaced with '{replace}'")

        found = True
        pos = idx + 1   # continue searching after this match (in case of overlaps)

if not found:
    print(f"[-] String '{search}' not found in heap")
else:
    print("[+] Done! Go look at ./main — it should now print your name")
