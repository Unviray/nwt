# -*- coding: utf-8 -*-

from pylev import damerau_levenshtein as lev


class GetDistance(object):
    def __init__(self, enter):
        self.enter = enter
        self.distance = 0

        dist_list = list()
        for book in book_list:
            dist_list.append(lev(book, self.enter))

        while True:
            try:
                self.closest = book_list[dist_list.index(self.distance)]
                break
            except ValueError:
                self.distance += 1

    def __len__(self):
        return self.distance

    def __str__(self):
        return self.closest


class Dir(object):
    import os
    from pathlib import Path

    prefix = Path(os.environ['PREFIX'])
    home = Path(os.path.expanduser('~'))

    sys_dir = prefix / 'share' / 'nwt/'
    home_dir = home / '.nwt/'
    cache_dir = home / '.cache' / 'nwt/'
    download_dir = cache_dir / 'download/'

    bible_dir = home_dir / 'bible/'
