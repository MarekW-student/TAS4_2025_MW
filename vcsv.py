#################### vcsv.py ####################

import csv
from faker import Faker

# get(self,column,row)
# - returns value stored in column and row of *.csv file
# - the first line is skipped (first line is header containing column names)
# - columns and rows counted from 0
# - None returned on error
#
# column_exists(self, name)
# - returns True when column with name exists in *.csv file
#
# column_index(self, name)
# - returns number of column with name
# - first column is 0
# - None returned when name not found in *.csv header
#
# _faker_value(self,value)
# - when value is special "##FAKER(name)##" or "##FAKER(password)##" return fake values generated by faker
# - for now only 2 fakes are supported: name and password

class CSVData:
    def __init__(self,filename):
        self.filename=filename
        with open(self.filename) as file_obj:
            self.reader_obj = csv.reader(file_obj)
            self.heading = next(self.reader_obj)
            self.list=list(self.reader_obj)
            self.lines= len(self.list)
        pass

    def column_exists(self, name):
        if name in self.heading: return True
        return False

    def column_index(self, name):
        if not self.column_exists(name): return None
        return self.heading.index(name)

    def _faker_value(self,value):
        if not value[:8] == "##FAKER(": return value
        test = value[-3:]
        if not value[-3:] == ")##": return value
        new_value = value[8:-3]
        match new_value:
            case "name":
                new_value = Faker().name()
            case "password":
                new_value = Faker().password()
            case _:
                new_value = value
        return new_value

    def get(self,column,row):
        if not self.column_exists(column): return None
        if row+1 > self.lines: return None
        line = self.list[row]
        index = self.column_index(column)
        value = line[self.column_index(column)]
        value = self._faker_value(value)
        return value

