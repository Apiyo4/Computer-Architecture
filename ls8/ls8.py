#!/usr/bin/env python3

"""Main."""

import sys
from cpu import CPU
if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} <filename>")
    sys.exit(1)
cpu = CPU()

cpu.load()
cpu.run()


