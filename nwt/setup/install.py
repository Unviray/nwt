#! -*- conding: utf-8 -*-
"""
Install bible
"""

import time
import shutil
import zipfile
from icecream import ic
from tinydb import TinyDB, Query
from bs4 import BeautifulSoup, NavigableString

from nwt.utils import Dir


class Install(object):
    def __init__(self, epubfile):
        if not zipfile.is_zipfile(epubfile):
            raise ValueError('Not a valid epub file')

        self.epubfile = epubfile
        self.zf = zipfile.ZipFile(epubfile, 'r')
        self.toc = self.zf.read('OEBPS/toc.xhtml')
        self.soup = BeautifulSoup(self.toc, "html.parser")
        self.bookList = {}
        self.metadata = {}

        self.metadata['title'] = self.soup.head.title.text
        self.metadata['stand'] = self.metadata['title'].split('(')[-1].split(')')[0]

        self.inspath = Dir.bible_dir / self.metadata['stand'].replace('-', '_')

        self.metadb = TinyDB(self.inspath / '{}.json'.format(
            self.metadata['stand']))

    def get_book_list(self):
        print('Get book list...', end=' ')

        bookDB = self.metadb.table('book_list')

        rawlist = self.soup.body.section.nav.ol.find_all('a')[1:133]
        for element in rawlist:
            if not ('Outline' in element.text):
                bookDB.insert(dict(
                    book_name=element.text,
                    book_path=element.attrs['href']))

                self.bookList[element.text] = element.attrs['href']
        print('done')

    def run(self):
        print('Copy file...', end=' ')
        shutil.copy(
            self.epubfile,
            self.inspath / '{}.epub'.format(self.metadata['stand']))
        print('done')

        self.get_book_list()
