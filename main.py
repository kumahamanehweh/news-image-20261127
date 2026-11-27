"""Entrypoint: render the newspaper into MAKEFUN_OUTPUT_DIR/entry.png."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import draw


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "entry.png")
    draw.render(path)
    size = os.path.getsize(path)
    print("wrote %s (%d bytes)" % (path, size))
    from PIL import Image
    with Image.open(path) as im:
        if im.size != (1024, 1024):
            raise SystemExit("bad output size: %r" % (im.size,))
    return path


if __name__ == "__main__":
    main()
