import re
import pandas as pd
import pandas.core.series
import openpyxl
from typing import List, Dict, Any

class ListRow:
    def __init__(self, listrowInfo):
        self.row__nf = listrowInfo.nf
        self.row__remote_host = listrowInfo.remote_host
        self.row__cNRF_AMF = listrowInfo.cNRF_AMF
        self.row__cNRF = listrowInfo.cNRF
        self.row__host = listrowInfo.host
        self.row__dn = listrowInfo.dn
        self.row__ns = listrowInfo.ns
        self.row__ip = listrowInfo.ip
        self.row__ver = int(listrowInfo.ver)
        self.row__region = listrowInfo.region
        self.row__del_flg = int(listrowInfo.del_flg)