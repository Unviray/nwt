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
            Dir.home_dir.mkdir(exist_ok=True)
            conf = toml.load(Dir.home_dir / 'config.toml')
        except toml.decoder.TomlDecodeError as error:
            raise ConfigError(error)
        except FileNotFoundError:
            conf_file = Dir.home_dir / "config.toml"
            conf_file.touch(exist_ok=True)
            self.__init__()

        self.bible_lang = conf.get('bible_lang', "bi12_MG")
