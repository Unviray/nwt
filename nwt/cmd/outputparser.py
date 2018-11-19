# -*- coding: utf-8 -*-
"""
Get data from base and for printing
"""
import textwrap
from icecream import ic
from bs4 import NavigableString

from nwt.bible import Epub
from nwt.config import Config
from nwt.utils import book_path
from nwt.utils import color_util as color
from nwt.cmd.inputparser import InputParser


def between(cur, end):
    """
    Get text between two different tag
    """

    while cur and cur != end:
        if isinstance(cur, NavigableString):
            text = cur.strip()
            if len(text):
                yield text
        cur = cur.next_element


def render(obj):
    '''
    obj
    ---
    { 'matio': {
        '24': {
            '14': 'Ary hotoriana...',
            '15': 'noho izany...',
            '16': 'dia aoka izay...',
        }
    }
    output
    ------
    Matio 24 14 Ary hotorina maneran-tany ity vaovao tsaran’ilay
           |  | fanjakana ity, ho vavolombelona amin’ny firenena rehetra,
           |  | vao ho tonga ny farany.
           | 15 noho izany
           | 16 dia aoka izany
    '''

    text = ''
    for book in obj:
        text += f'{color.blue(book.title())} '
        lenbook = len(book)
        for chapter in obj[book]:
            text += f'{color.green(chapter)} '
            lenchapter = len(str(chapter))
            for verset in obj[book][chapter]:
                text += f'{color.red(verset)} '
                lenverset = len(str(verset))
                wtext = textwrap.wrap(obj[book][chapter][verset], 60)
                for line in wtext:
                    text += (line + '\n' + (
                        ' ' * (lenbook + lenchapter)) + color.green('|') +
                                    (' ' * lenverset) + color.red('|') + ' ')
                text += ('\n' + (' ' * (lenbook + lenchapter)) +
                                color.green('|') + ' ')
            text += ('\n' + (' ' * (lenbook + lenchapter)))

    return text


class FileHandler:
    def __init__(self):
        self._book = ''
        self._chap = 0
        self._vers = 0
        self.book_file = ''
        self.chap_file = ''

    def book(self, b_arg):
        self._book = b_arg

        b_file = book_path(b_arg)[0]["book_path"]
        self.book_file = f'OEBPS/{b_file}'

    def chapter(self, c_arg):
        epub = Epub(self.book_file)
        elements = epub.souped().body.table.find_all('a')

        self._chap = int(c_arg)

        c_file = elements[int(c_arg) - 1].attrs['href']
        self.chap_file = f'OEBPS/{c_file}'

    def verset(self, v_arg):
        epub = Epub(self.chap_file)

        tag = u"chapter{}_verse{}"
        start = tag.format(str(self._chap), str(v_arg))
        end = tag.format(str(self._chap), str(int(v_arg) + 1))

        return ' '.join(
            _ for _ in between(
                epub.souped().find("span", attrs={"id": start}).next_sibling,
                epub.souped().find("span", attrs={"id": end})))


class OutputParser:
    def __init__(self, query):
        self.query = query
        self.text = ''

        if not isinstance(self.query, InputParser):
            raise ValueError('query must be InputParser obj')

        self.new_dict = dict()
        query = self.query.result
        file_handler = FileHandler()

        for book in query:

            self.new_dict[book] = dict()
            file_handler.book(book)

            for chapter in query[book]:

                self.new_dict[book][chapter] = dict()
                file_handler.chapter(chapter)

                for verset in query[book][chapter]:

                    ptext = file_handler.verset(verset)
                    self.new_dict[book][chapter][verset] = ptext

    def __str__(self):
        return render(self.new_dict)
