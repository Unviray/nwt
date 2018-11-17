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

from nwt.utils.os_util import Dir


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
        self.metadata['stand'] = self.metadata['title'].split('(')[-1]
        self.metadata['stand'] = self.metadata['stand'].split(')')[0]
        self.metadata['stand'] = self.metadata['stand'].replace('-', '_')

        self.inspath = Dir.bible_dir / self.metadata['stand'].replace('-', '_')

        self.metadb = TinyDB(self.inspath / '{}.json'.format(
            self.metadata['stand']))

    def get_book_list(self):
        bookDB = self.metadb.table('book_list')

        rawlist = self.soup.body.section.nav.ol.find_all('a')[1:133]
        for element in rawlist:
            if not 'Outline' in element.text:
                bookDB.insert(dict(
                    book_name=element.text,
                    book_path=element.attrs['href']))

                self.bookList[element.text] = element.attrs['href']

    def run(self):
        print('Copy file...', end=' ')
        shutil.copy(
            self.epubfile,
            self.inspath / '{}.epub'.format(self.metadata['stand']))
        print('done')

        print('Get book list...', end=' ')
        self.get_book_list()
        print('done')
