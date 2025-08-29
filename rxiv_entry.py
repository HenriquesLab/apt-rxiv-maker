#!/usr/bin/env python3
"""Entry point script for rxiv PyInstaller binary."""

import sys
from rxiv_maker.cli import main

if __name__ == "__main__":
    sys.exit(main())