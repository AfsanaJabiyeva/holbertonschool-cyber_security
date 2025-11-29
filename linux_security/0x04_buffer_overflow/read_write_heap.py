#!/usr/bin/python3
"""
read_write_heap.py - Find and replace an ASCII string in the heap of a process

Usage:
    read_write_heap.py <pid> <search_string> <replace_string>

This script only searches and modifies memory inside the [heap] region.
It requires root privileges or CAP_SYS_PTRACE (in lab containers you usually
need to run:  echo 0 > /proc/sys/kernel/yama/ptrace_scope  first).
"""
import sys
import os


def print_usage():
    """Print usage information and exit with error code 1."""
    print("Usage: read_write_heap.py pid search_string replace_string",
          file=sys.stderr)
    sys.exit(1)


def main():
    """Main function - parse arguments and perform heap string replacement."""
    if len(sys.argv) != 4:
        print_usage()

    try:
        pid = int(sys.argv[1])
    except ValueError:
        print("Error: pid must be an integer", file=sys.stderr)
        sys.exit(1)

    search_str = sys.argv[2]
    replace_str = sys.argv[3]

    # Ensure strings are pure ASCII (task requirement)
    try:
        search_bytes = search_str.encode('ascii')
        replace_bytes = replace_str.encode('ascii')
    except UnicodeEncodeError:
        print("Error: strings must contain ASCII characters only", file=sys.stderr)
        sys.exit(1)

    if not search_bytes:
        print("Error: search string cannot be empty", file=sys.stderr)
        sys.exit(1)

    # Do not allow replacement longer than original → prevents real overflow
    if len(replace_bytes) > len(search_bytes):
        print("Error: replacement string cannot be longer than search string",
              file=sys.stderr)
        sys.exit(1)

    maps_path = "/proc/{}/maps".format(pid)
    mem_path = "/proc/{}/mem".format(pid)

    # Find heap boundaries
    heap_start = heap_end = None
    try:
        with open(maps_path, "r") as maps:
            for line in maps:
                if "[heap]" in line:
                    addr = line.split()[0]
                    heap_start = int(addr.split("-")[0], 16)
                    heap_end = int(addr.split("-")[1], 16)
                    print("Found heap: {:#x}-{:#x}".format(heap_start, heap_end))
                    break
        if heap_start is None:
            print("Error: no heap found for PID {}".format(pid), file=sys.stderr)
            sys.exit(1)
    except (IOError, OSError):
        print("Error: cannot read /proc/{}/maps (process gone or permission denied)"
              .format(pid), file=sys.stderr)
        sys.exit(1)

    # Open process memory for reading and writing
    try:
        mem = open(mem_path, "rb+")
    except (IOError, OSError):
        print("Error: cannot open /proc/{}/mem - try: echo 0 > /proc/sys/kernel/yama/ptrace_scope"
              .format(pid), file=sys.stderr)
        sys.exit(1)

    found = False
    with mem:
        # Read entire heap at once (heap is usually small)
        mem.seek(heap_start)
        heap_data = mem.read(heap_end - heap_start)

        pos = 0
        while True:
            idx = heap_data.find(search_bytes, pos)
            if idx == -1:
                break

            address = heap_start + idx
            print("Found \"{}\" at {:#x}".format(search_str, address))

            # Build replacement with proper null termination and padding
            padding = b"\x00" * (len(search_bytes) - len(replace_bytes))
            new_data = replace_bytes + padding

            mem.seek(address)
            mem.write(new_data)
            print("  → replaced with \"{}\"".format(replace_str))

            found = True
            pos = idx + 1   # continue searching (allows overlapping matches)

    if not found:
        print("String \"{}\" not found in heap".format(search_str))
    else:
        print("Success! Check the target process output.")


if __name__ == "__main__":
    main()
