"""Configure sys.path so the solution tests import from solution/src."""
import sys
from pathlib import Path

# Insert solution/src at the front so it takes precedence over the starter src/
sys.path.insert(0, str(Path(__file__).parent / "src"))
