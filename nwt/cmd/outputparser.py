# -*- coding: utf-8 -*-
"""
Get data from base and for printing
"""

from nwt.cmd.inputparser import InputParser


class OutputParser(object):
    def __init__(self, query):
        self.query = query
        self.text = ''

        if not isinstance(self.query, InputParser):
            raise ValueError('query must be InputParser obj')

        query = self.query.result
        for book in query:
            for chapter in query[book]:
                for verset in query[book][chapter]:
                    print(book, chapter, verset)
