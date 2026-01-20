from dataclasses import dataclass
from typing import List


@dataclass
class ConfigLine:
    lineno: int
    line: str


def parse_config_file(path: str) -> List[ConfigLine]:
    """
    Reads a config file and returns normalized non-empty lines with line numbers.
    Very simple parser: no vendor-specific grammar, just clean lines.
    """
    items: List[ConfigLine] = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for idx, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            # Optional: skip common comment styles
            if line.startswith("!"):
                continue
            items.append(ConfigLine(lineno=idx, line=line))
    return items
