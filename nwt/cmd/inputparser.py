# -*- coding: utf-8 -*-
"""
The parser for all input query
"""

import collections

from nwt.errors import InputError
from nwt.utils import GetDistance


def parse_int_list(range_string, delim=',', range_delim='-'):
    """
    Returns a sorted list of positive integers based on
    *range_string*. Reverse of :func:`format_int_list`.

    Args:
        range_string (str):
            String of comma separated positive integers or ranges
            (e.g. '1,2,4-6,8'). Typical of a custom page range string used
            in printer dialogs.

        delim (char):
            Defaults to ','. Separates integers and contiguous ranges of
            integers.

        range_delim (char):
            Defaults to '-'. Indicates a contiguous range of integers.

    >>> parse_int_list('1,3,5-8,10-11,15')
    [1, 3, 5, 6, 7, 8, 10, 11, 15]
    """
    output = []

    for element in range_string.strip().split(delim):

        # Range
        if range_delim in element:
            range_limits = list(map(int, element.split(range_delim)))
            output += list(range(min(range_limits), max(range_limits)+1))

        # Empty String
        elif not element:
            continue

        # Integer
        else:
            output.append(int(element))

    return sorted(output)


def format_int_list(int_list, delim=',', range_delim='-', delim_space=False):
    """
    Returns a sorted range string from a list of positive integers
    (*int_list*). Contiguous ranges of integers are collapsed to min
    and max values. Reverse of :func:`parse_int_list`.

    Args:
        int_list (list):
            List of positive integers to be converted into a range string
            (e.g. [1,2,4,5,6,8]).

        delim (char):
            Defaults to ','. Separates integers and contiguous ranges of
            integers.

        range_delim (char):
            Defaults to '-'. Indicates a contiguous range of integers.

        delim_space (bool):
            Defaults to ``False``. If ``True``, adds a space after all
            *delim* characters.

    >>> format_int_list([1,3,5,6,7,8,10,11,15])
    '1,3,5-8,10-11,15'
    """
    output = []
    contig_range = collections.deque()

    for x in sorted(int_list):

        # Handle current (and first) value.
        if len(contig_range) < 1:
            contig_range.append(x)

        # Handle current value, given multiple previous values are contiguous.
        elif len(contig_range) > 1:
            delta = x - contig_range[-1]

            # Current value is contiguous.
            if delta == 1:
                contig_range.append(x)

            # Current value is non-contiguous.
            elif delta > 1:
                range_substr = '{0:d}{1}{2:d}'.format(min(contig_range),
                                                      range_delim,
                                                      max(contig_range))
                output.append(range_substr)
                contig_range.clear()
                contig_range.append(x)

            # Current value repeated.
            else:
                continue

        # Handle current value, given no previous contiguous integers
        else:
            delta = x - contig_range[0]

            # Current value is contiguous.
            if delta == 1:
                contig_range.append(x)

            # Current value is non-contiguous.
            elif delta > 1:
                output.append('{0:d}'.format(contig_range.popleft()))
                contig_range.append(x)

            # Current value repeated.
            else:
                continue

    # Handle the last value.
    else:

        # Last value is non-contiguous.
        if len(contig_range) == 1:
            output.append('{0:d}'.format(contig_range.popleft()))
            contig_range.clear()

        # Last value is part of contiguous range.
        elif len(contig_range) > 1:
            range_substr = '{0:d}{1}{2:d}'.format(min(contig_range),
                                                  range_delim,
                                                  max(contig_range))
            output.append(range_substr)
            contig_range.clear()

    if delim_space:
        output_str = (delim+' ').join(output)
    else:
        output_str = delim.join(output)

    return output_str


class InputParser:
    """
    Parse simple inline query
    """
    def __init__(self, query):
        self.query = query
        self.result = {}

        def parse():
            """
            Auto parse query
            """

            # separate book and pointers
            pbook = self.query.lower().split(' ')
            prebook1 = GetDistance(pbook[0])
            prebook2 = GetDistance(' '.join(pbook[:1]))

            if not isinstance(pbook, list):
                raise InputError('Please add an space in your input')

            # get closest distance between 'have space' or 'haven't'
            if prebook1.distance <= prebook2.distance:
                entbook = prebook1
            else:
                entbook = prebook2

            # if have space the pointer is in index 2
            with_sub = len(entbook.closest.split(' ')) > 1

            if with_sub:
                rawsubbook = pbook[2]
            else:
                rawsubbook = pbook[1]

            # decode pointers
            subbook = dict()
            for raw in rawsubbook.split(';'):
                chapter = int(raw.split(':')[0])
                verset = parse_int_list(raw.split(':')[1])
                subbook[chapter] = verset

            self.result[entbook.closest] = subbook

        parse()

    def __str__(self):
        _str = str()
        for book in self.result:
            _str += (book + ' ')
            for chapter in self.result[book]:
                _str += (str(chapter) + ':')
                _str += format_int_list(
                    [_ for _ in self.result[book][chapter]])
                _str += ';'
            _str = _str[:-1]
        return _str

    def __repr__(self):
        return repr(self.result)

    def __len__(self):
        _len = 0
        for book in self.result:
            for chapter in self.result[book]:
                for _ in self.result[book][chapter]:
                    _len += 1
        return _len
