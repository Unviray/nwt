#!/usr/bin/env python
# -*- coding: utf-8 -*-

COMMANDS = {
    # Lables
    'info': (33, '[!] '),
    'que': (34, '[?] '),
    'bad': (31, '[-] '),
    'good': (32, '[+] '),
    'run': (97, '[~] '),

    # Colors
    'green': 32,
    'lightgreen': 92,
    'grey': 37,
    'black': 30,
    'red': 31,
    'lightred': 91,
    'cyan': 36,
    'lightcyan': 96,
    'blue': 34,
    'lightblue': 94,
    'purple': 35,
    'yellow': 93,
    'white': 97,
    'lightpurple': 95,
    'orange': 33,

    # Styles
    'bg': ';7',
    'bold': ';1',
    'italic': '3',
    'under': '4',
    'strike': '09',
}


def _gen(string, prefix, key):
    colored = prefix if prefix else string
    not_colored = string if prefix else ''
    return '\033[{}m{}\033[0m{}'.format(key, colored, not_colored)


for key, val in COMMANDS.items():
    value = val[0] if isinstance(val, tuple) else val
    prefix = val[1] if isinstance(val, tuple) else ''
    locals()[key] = lambda s, prefix=prefix, key=value: _gen(s, prefix, key)

__all__ = list(COMMANDS.keys())
