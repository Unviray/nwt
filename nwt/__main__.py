# -*- coding: utf-8 -*-
"""
Entry point for launching nwt by python command
`python -m nwt`
"""

import sys

from nwt.cli import main


if __name__ == '__main__':
    sys.exit(main())
