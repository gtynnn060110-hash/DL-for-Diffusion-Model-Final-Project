"""Add the repository root to sys.path so that ``rectified_flow`` is importable.

Usage — place this at the very top of every script inside ``scripts/``::

    import _bootstrap  # noqa: E402, F401 — must precede rectified_flow imports
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
