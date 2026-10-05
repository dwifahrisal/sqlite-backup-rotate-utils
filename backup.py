#!/usr/bin/env python3
"""Backup a SQLite database safely and prune backups older than N days."""

import datetime as dt
import os
import subprocess
import sys

DB_PATH = sys.argv[1] if len(sys.argv) > 1 else "app.db"
OUT_DIR = sys.argv[2] if len(sys.argv) > 2 else "backups"
KEEP_DAYS = int(sys.argv[3]) if len(sys.argv) > 3 else 7


def main() -> int:
    os.makedirs(OUT_DIR, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(OUT_DIR, f"{os.path.basename(DB_PATH)}.{stamp}")

    proc = subprocess.run(
        ["sqlite3", DB_PATH, f".backup '{dest}'"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        print(f"backup failed: {proc.stderr}", file=sys.stderr)
        return 1
    print(f"backup -> {dest}")

    now = dt.datetime.now()
    for name in sorted(os.listdir(OUT_DIR)):
        full = os.path.join(OUT_DIR, name)
        mtime = dt.datetime.fromtimestamp(os.path.getmtime(full))
        if (now - mtime).days > KEEP_DAYS:
            os.remove(full)
            print(f"pruned: {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
