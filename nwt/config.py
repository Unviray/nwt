"""
    nwt.config
    ----------

    get a configuration from file
"""

import os
import toml
import traceback
import contextlib

from nwt.utils.os_util import Dir
from nwt.errors import ConfigError


class Config:
    def __init__(self):
        try:
            conf = toml.load(Dir.home_dir / 'config.toml')
        except toml.decoder.TomlDecodeError as error:
            raise ConfigError(error)

        self.bible_lang = conf['bible_lang'] or []
