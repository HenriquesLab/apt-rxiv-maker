#!/usr/bin/env python3
"""Entry point script for rxiv-install-deps PyInstaller binary."""

import sys
from rxiv_maker.install.manager import main

if __name__ == "__main__":
    sys.exit(main())