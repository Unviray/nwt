# -*- coding: utf-8 -*-

from tinydb import TinyDB, Query
from pylev import damerau_levenshtein as lev

from nwt.config import Config
from nwt.utils.os_util import Dir


def book_path(book_arg) -> dict:
    bible_lang = Config().bible_lang
    db = TinyDB(Dir.bible_dir / bible_lang / '{}.json'.format(bible_lang))
    book_list = db.table('book_list')
    query = Query()

    return book_list.search(query.book_name == book_arg)


def get_book_list():
    bible_lang = Config().bible_lang
    db = TinyDB(Dir.bible_dir / bible_lang / '{}.json'.format(bible_lang))
    bookList = db.table('book_list')
    book_list = [_['book_name'] for _ in bookList]

    return book_list


class GetDistance(object):
    def __init__(self, enter):
        self.enter = enter
        self.distance = 0
        book_list = get_book_list()

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
