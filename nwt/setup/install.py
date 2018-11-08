# -*- conding: utf-8 -*-
"""
Install bible
"""

import time
import zipfile
from icecream import ic
from tinydb import TinyDB
from bs4 import BeautifulSoup

from nwt.utils import Dir


class Install(object):
    def __init__(self, epubfile):
        if not zipfile.is_zipfile(epubfile):
            raise ValueError('Not a valid epub file')

        self.zf = zipfile.ZipFile(epubfile, 'r')
        self.toc = self.zf.read('OEBPS/toc.xhtml')
        self.soup = BeautifulSoup(self.toc, "html.parser")
        self.bookList = {}
        self.metadata = {}

        self.metadata['title'] = self.soup.head.title.text
        self.metadata['stand'] = self.metadata['title'].split('(')[-1].split(')')[0]

        self.inspath = Dir.bible_dir / self.metadata['stand'].replace('-', '_')

    def get_book_list(self):
        print('Get book list...', end='')

        rawlist = self.soup.body.section.nav.ol.find_all('a')[1:133]
        for element in rawlist:
            if not ('Outline' in element.text):
                self.bookList[element.text] = element.attrs['href']
        time.sleep(1)
        print('done')

    def process_book(self, bookname, xpoint):
        print(bookname, end=' ')
        dbBook = TinyDB(self.inspath / '{}.json'.format(bookname))

        chapp = self.zf.read('OEBPS/' + xpoint)
        chapters = []

        chaplist = chapp.body.table.find_all('a')
        for line in chaplist:
            chapters.append(line.attrs['href'])

    def process_chapter(self, dbBook, num, xpoint):
        chapter = dbBook.table(str(num))

