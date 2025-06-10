#################### vini.py ####################

import configparser
from configparser import ConfigParser
import os

# set of functions reading from *.ini files
# sample ini file structure:
# [section1]
# key1=value1
# key2=value2
# [section5]
# key1=value7
#
# if *.ini filename is not specified by default "webshop.ini" is used with path same like *.py 
#
# read_string_from_ini( self, section, key )
# - returns string value of "key" under "section"
# - on error returns empty string
#
# read_boolean_from_ini( self, section, key )
# - returns converted to boolen value of "key" under "section"
# - values: 1, true (regardless of the letter case) are converted to True
# - values: 0, false (regardless of the letter case) are converted to False
# - on error returns False
#
# read_float_from_ini( self, section, key )
# - returns converted to float value of "key" under "section"
# - on error returns empty string
#
# get_full_path( self )
# - returns full path to *.ini file

class Vini:
    def __init__(self, filename = None):
        self.fullfilepath = os.path.join( os.path.dirname(os.path.abspath(__file__)), "webshop.ini" )
        if filename is not None:
            self.fullfilepath = filename
        self.config = ConfigParser()
        self.config.read( self.fullfilepath )

    def get_full_path( self ):
        return self.fullfilepath

    def read_float_from_ini( self, section, key ):
        if section not in self.config.sections():
            return ""
        try:
            self.value = self.config.getfloat( section, key )
        except (configparser.NoOptionError, configparser.NoSectionError):
            self.value = 0.0
        return self.value

    def read_string_from_ini( self, section, key ):
        if section not in self.config.sections():
            return ""
        try:
            self.value = self.config.get( section, key )
        except (configparser.NoOptionError, configparser.NoSectionError):
            self.value = ""
        return self.value

    def read_boolean_from_ini( self, section, key ):
        if section not in self.config.sections():
            return False
        try:
            self.value = self.config.getboolean( section, key )
        except (configparser.NoOptionError, configparser.NoSectionError):
            self.value = False
        return self.value

