import re
import pandas as pd
import pandas.core.series
import openpyxl
from typing import List, Dict, Any

from MainRow import MainRow
# from SubRow import SubRow
from ListRow import ListRow

from MM_ListConfig import ListConfig

main_cnt = 0
sub_cnt = 0
list_cnt = 0

class MM_ConfigNext:

    def main_next(config_info):
        global main_cnt
        mainrow_info = MainRow(config_info.mainConfigs[main_cnt])
        main_cnt += 1
        return mainrow_info

    # def sub_next(config_info):
    #     global sub_cnt
    #     subrow_info = SubRow(config_info.subConfigs[sub_cnt])
    #     sub_cnt += 1
    #     return subrow_info

    def list_next(config_info):
        global list_cnt
        listrow_info = ListRow(config_info.listConfigs[list_cnt])
        list_cnt += 1
        return listrow_info