import re
import pandas as pd
import pandas.core.series
import openpyxl
from typing import List, Dict, Any

cNRF_list = []
cNRF_AMF_list = []
DEL_FLG_list = []
DN_list = []
HOST_list = []
IP_list = []
NF_list = []
NS_list = []
REGION_list = []
REMOTE_HOST_list = []
VER_list = []

class ListConfig:
    """接続設定情報

    NF設備への接続のための設定を保持する

    """

    def __init__(self, nf: str, remote_host:str, cNRF_AMF: str, cNRF: str, host:str,
                 dn: str, ns: str, ip: str, ver: int, region: str, del_flg: int) -> None:
        """初期化

        Args:
            nf (str): コマンド実行対象ホスト名 コマンドを実行する対象となるホスト名
            remote_host(str): SSH接続ホスト名 SSH接続を行うホスト名
            cNRF_AMF(str): cNFR-AMFホスト名 cNRFホストが接続するAMFホスト名を示した情報
            cNRF(str): cNRFホスト名 cNRFのホスト名
            host(str): AMFホスト名 AMFのホスト名
            dn (str): ドメイン名
            ns (str): ネットワークシステム名
            ip (str): 接続先IPアドレス
            ver (int): 
            region(str): 実行地域
            del_flg(int): 

        """

        global cNRF_list
        global cNRF_AMF_list
        global DEL_FLG_list
        global DN_list
        global HOST_list
        global IP_list
        global NF_list
        global NS_list
        global REGION_list
        global REMOTE_HOST_list
        global VER_list

        self.__nf: str = nf
        ListConfig.append__nf(self.__nf)

        self.__remote_host: str = remote_host
        ListConfig.append__remote_host(self.__remote_host)

        self.__cNRF_AMF: str = cNRF_AMF
        ListConfig.append__cNRF_AMF(self.__cNRF_AMF)

        self.__cNRF: str = cNRF
        ListConfig.append__cNRF(self.__cNRF)

        self.__host:str = host
        ListConfig.append__host(self.__host)

        self.__dn: str = dn
        ListConfig.append__dn(self.__dn)

        self.__ns: str = ns
        ListConfig.append__ns(self.__ns)

        self.__ip: str = ip
        ListConfig.append__ip(self.__ip)

        self.__ver: int = int(ver)
        ListConfig.append__ver(self.__ver)

        self.__region: str = region
        ListConfig.append__region(self.__region)

        self.__del_flg: int = int(del_flg)
        ListConfig.append__del_flg(self.__del_flg)


    @property
    def nf(self) -> str:
        """コマンド実行対象ホスト名プロパティ

        インスタンス属性のコマンド実行対象ホスト名を取得する

        Returns:
            str: インスタンス属性のコマンド実行対象ホスト名
        """
        return self.__nf

    def append__nf(val):
        NF_list.append(val)
    
    def get__nf_list():
        return NF_list

    def get__row_nf(row):
        return NF_list[row]



    @property
    def remote_host(self) -> str:
        """SSH接続ホスト名プロパティ

        インスタンス属性のSSH接続ホスト名を取得する

        Returns:
            str: インスタンス属性のSSH接続ホスト名
        """
        return self.__remote_host

    def append__remote_host(val):
        REMOTE_HOST_list.append(val)
    
    def get__remote_host_list():
        return REMOTE_HOST_list

    def get__row_remote_host(row):
        return REMOTE_HOST_list[row]



    @property
    def cNRF_AMF(self) -> str:
        """

        """
        return self.__cNRF_AMF

    def append__cNRF_AMF(val):
        cNRF_AMF_list.append(val)
    
    def get__cNRF_AMF_list():
        return cNRF_AMF_list

    def get__row_cNRF_AMF(row):
        return cNRF_AMF_list[row]



    @property
    def cNRF(self) -> str:
        """
        
        """
        return self.__cNRF

    def append__cNRF(val):
        cNRF_list.append(val)
    
    def get__cNRF_list():
        return cNRF_list

    def get__row_cNRF(row):
        return cNRF_list[row]



    @property
    def host(self) -> str:
        """
        
        """
        return self.__host

    def append__host(val):
        HOST_list.append(val)
    
    def get__host_list():
        return HOST_list

    def get__row_host(row):
        return HOST_list[row]


    @property
    def dn(self) -> str:
        """プロパティ

        インスタンス属性のを取得する

        Returns:
            str: インスタンス属性の
        """
        return self.__dn
    
    def append__dn(val):
        DN_list.append(val)
    
    def get__dn_list():
        return DN_list

    def get__row_dn(row):
        return DN_list[row]


    @property
    def ns(self) -> str:
        """プロパティ

        インスタンス属性のを取得する

        Returns:
            str: インスタンス属性の
        """
        return self.__ns

    def append__ns(val):
        NS_list.append(val)
    
    def get__ns_list():
        return NS_list

    def get__row_ns(row):
        return NS_list[row]


    @property
    def ip(self) -> str:
        """接続先IPプロパティ

        インスタンス属性の接続先IPを取得する

        Returns:
            str: インスタンス属性の接続先IP
        """
        return self.__ip

    def append__ip(val):
        IP_list.append(val)
    
    def get__ip_list():
        return IP_list

    def get__row_ip(row):
        return IP_list[row]


    @property
    def ver(self) -> int:
        """プロパティ

        インスタンス属性のを取得する

        Returns:
            bool: インスタンス属性の
        """
        return self.__ver

    def append__ver(val):
        VER_list.append(val)
    
    def get__ver_list():
        return VER_list

    def get__row_ver(row):
        return VER_list[row]


    @property
    def region(self) -> str:
        """実行地域プロパティ

        インスタンス属性の実行地域を取得する

        Returns:
            bool: インスタンス属性の実行地域
        """
        return self.__region

    def append__region(val):
        REGION_list.append(val)
    
    def get__region_list():
        return REGION_list

    def get__row_region(row):
        return REGION_list[row]


    @property
    def del_flg(self) -> int:
        """プロパティ

        インスタンス属性のを取得する

        Returns:
            int: インスタンス属性の
        """
        return self.__del_flg

    def append__del_flg(val):
        DEL_FLG_list.append(val)
    
    def get__del_flg_list():
        return DEL_FLG_list

    def get__row_del_flg(row):
        return DEL_FLG_list[row]


    def __str__(self) -> str:
        """インスタンスの文字列表示

        インスタンス属性の名前と値を表示する

        Returns:
            str: インスタンス属性の名前と値を表示した文字列
        """
        return str(vars(self))
    

    def __repr__(self) -> str:
        """インスタンスの文字列表現

        本来の文字列表現ではなく__str__()と同様の文字列とする

        Returns:
            str: __str__()が返却する文字列
        """
        return self.__str__()

    def __eq__(self, __o: object) -> bool:
        """等価演算子

        比較対象オブジェクトが自身と等価かどうかを判定する
        同一クラスかつインスタンス変数がすべて等価の場合等価とする

        Args:
            __o (object): 比較対象オブジェクト

        Returns:
            bool: 比較対象オブジェクトが自身と等価の場合true 等価でない場合false
        """
        if not isinstance(__o, self.__class__):
            return NotImplemented
        return self.__dict__ == __o.__dict__
