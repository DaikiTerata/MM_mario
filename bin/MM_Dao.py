import re
import pandas as pd
import pandas.core.series
import openpyxl
from typing import List, Dict, Any

from MM_MainLoadConfig import MainLoadConfig
from MM_SubLoadConfig import SubLoadConfig
from MM_ListLoadConfig import ListLoadConfig
from MM_ConfigNext import MM_ConfigNext
from MainRow import MainRow

mainconfigFile = "C:\\python\\MM_scenario_config.xlsx"
subconfigFile = "C:\\python\\MM_scenario_config.xlsx"
listconfigFile = "C:\\python\\MM_scenario_config.xlsx"

class MM_Dao:

    def load(config_name: str):

        if config_name == "main":
            config = MainLoadConfig(mainconfigFile)

        elif config_name == "sub":
            config = SubLoadConfig(subconfigFile)

        elif config_name == "list":
            config = ListLoadConfig(listconfigFile)
        
        return config
    
    def main_next(config_info):
        row_config = MM_ConfigNext.main_next(config_info)
        return row_config
    
    # def sub_next(config_info):
    #     row_config = MM_ConfigNext.sub_next(config_info)
    #     return row_config

    def list_next(config_info):
        row_config = MM_ConfigNext.list_next(config_info)
        return row_config


if __name__ == '__main__':
    MM_main_config = MM_Dao.load("main")
    MM_list_config = MM_Dao.load("list")

    main_config_len = len(MM_main_config.mainConfigs)
    list_config_len = len(MM_list_config.listConfigs)

    mainrow_config = MM_Dao.main_next(MM_main_config)
    print(mainrow_config.mainrowKey, mainrow_config.mainrowValue)
    listrow_config = MM_Dao.list_next(MM_list_config)
    print(listrow_config)
    # row_config = MM_Dao.main_next(MM_main_config)
    # print(row_config.mainrowKey, row_config.mainrowValue)
    # row_keylist = MainKey.get_mainKeylist()
    # print(row_keylist)
    # for i in range(main_config_len):
    #     row_config = MM_Dao.main_next(MM_main_config)
    #     row_keylist = MainRow.get_mainKeylist()
    #     row_valuelist = MainRow.get_mainValuelist()
    #     if i == 7:
    #         row_mainkey = MainRow.get_row_mainkey(2)
    #         print("#######")
    #         print(row_mainkey)
    #         print("#######")
    #     print(row_config.mainrowKey, row_config.mainrowValue)
    #     print(row_keylist)
    #     print()
    #     print(row_valuelist)
    #     print()
    #     print()

    # print(row_keylist)
    # print()
    # print()
    # print(row_valuelist)
    # print()
    # print()
    # config = MM_config.load(config_sheet)
    # print(MM_main_config)
    # print(len(MM_main_config.mainConfigs))
    # print(type(MM_main_config.mainConfigs))
    # # cnt = 0
    # for i in MM_main_config.mainConfigs:
    #     print(i)
    # for key, val in MM_main_config.mainConfigs.items():
    #     print(key, val)
    #     # print(key)
    #     # print(val._MainConfig__value)
    #     print()
    #     print()