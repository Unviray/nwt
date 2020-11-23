# -*- coding: utf-8 -*-

import os
from pathlib import Path

class Dir(object):
    prefix = Path(os.environ.get('PREFIX', "/usr"))
    home = Path(os.path.expanduser('~'))

    sys_dir = prefix / 'share' / 'nwt/'
    home_dir = home / '.nwt/'
    cache_dir = home / '.cache' / 'nwt/'
    download_dir = cache_dir / 'download/'

    bible_dir = home_dir / 'bible/'
