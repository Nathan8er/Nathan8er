#!/usr/bin/env python3
"""
Increments a counter, writes it to counter.txt, and injects the
current values into README.md between marker comments.

Run locally with:  python scripts/update_counter.py
"""

import re
from datetime import datetime, timezone, date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNTER_FILE = ROOT / "counter.txt"
README_FILE = ROOT / "README.md"

# Change this to whenever you want "days coding" measured from
START_DATE = date(2018, 1, 1)


def read_counter() -> int:
    """Read the current count, defaulting to 0 if the file is missing or junk."""
    if not COUNTER_FILE.exists():
        return 0
    try:
        return int(COUNTER_FILE.read_text().strip())
    except ValueError:
        print("counter.txt was unreadable — resetting to 0")
        return 0


def write_counter(count: int) -> None:
    COUNTER_FILE.write_text(f"{count}\n")


def update_readme(count: int, stamp: str, days: int) -> bool:
    """Replace the block between the marker comments. Returns True if changed."""
    if not README_FILE.exists():
        print("No README.md found — skipping injection")
        return False

    content = README_FILE.read_text()

    block = (
        f"<!--COUNTER:START-->\n"
        f"`updates: {count}` &nbsp;·&nbsp; "
        f"`days coding: {days:,}` &nbsp;·&nbsp; "
        f"`last refresh: {stamp} UTC`\n"
        f"<!--COUNTER:END-->"
    )

    pattern = re.compile(
        r"<!--COUNTER:START-->.*?<!--COUNTER:END-->",
        re.DOTALL,
    )

    if not pattern.search(content):
        print("Marker comments not found in README.md — skipping injection")
        return False

    updated = pattern.sub(block, content)
    if updated == content:
        return False

    README_FILE.write_text(updated)
    return True


def main() -> None:
    count = read_counter() + 1
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    days = (date.today() - START_DATE).days

    write_counter(count)
    injected = update_readme(count, stamp, days)

    print(f"counter  -> {count}")
    print(f"days     -> {days}")
    print(f"stamp    -> {stamp} UTC")
    print(f"readme   -> {'updated' if injected else 'unchanged'}")


if __name__ == "__main__":
    main()
