#!/usr/bin/env python3
"""Copy the bundled entry.png to MAKEFUN_OUTPUT_DIR (stdlib only)."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    size = os.path.getsize(dst)
    if size > 1048576:
        print("entry.png exceeds 1 MiB:", size, file=sys.stderr)
        return 1
    print("wrote", dst, "(%d bytes)" % size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
