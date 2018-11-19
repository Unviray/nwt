# -*- coding: utf-8 -*-
"""
The layer betwenn nwt and epub bible
"""
from bs4 import BeautifulSoup
import zipfile

from nwt.utils.os_util import Dir
from nwt.config import Config


conf = Config()


class Epub:
    b_path = Dir.bible_dir / conf.bible_lang / f'{conf.bible_lang}.epub'

    def __init__(self, init_file=None):
        self.init_file = init_file
        self.z = zipfile.ZipFile(self.b_path, 'r')

    def read(self, requested_file=None):
        return self.z.read(requested_file or self.init_file)

    def souped(self, requested_file=None):
        return BeautifulSoup(self.read(requested_file or self.init_file),
                             "html.parser")
