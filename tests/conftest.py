"""Make `pytest` import this checkout's src/ ahead of any installed copy of skillcard."""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if _SRC.is_dir():
    sys.path.insert(0, str(_SRC))
