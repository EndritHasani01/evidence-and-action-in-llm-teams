"""Source-checkout wrapper. The installed equivalent is `i01-course`."""
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from recovery.i01.cli import main

if __name__=="__main__":
    main()
