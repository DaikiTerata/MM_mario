import re
import pandas as pd
import pandas.core.series
import openpyxl
from typing import List, Dict, Any

key_list = []
value_list = []

class MainRow:

    def __init__(self, mainrowInfo):
        global key_list
        global value_list
        self.mainrowKey = mainrowInfo.key
        MainRow.append_key(self.mainrowKey)

        self.mainrowValue = mainrowInfo.value
        MainRow.append_value(self.mainrowValue)


    def append_key(key):
        key_list.append(key)
    
    def get_key_list():
        return key_list
    
    def get_row_mainkey(row):
        row_mainKey = key_list[row]
        return row_mainKey


    def append_value(value):
        value_list.append(value)
    
    def get_value_list():
        global value_list
        return value_list

    def get_row_mainvalue(row):
        row_mainValue = value_list[row]
        return row_mainValue
    