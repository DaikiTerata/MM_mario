import re
import pandas as pd
import pandas.core.series
import openpyxl
from typing import List, Dict, Any


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
        self.__nf: str = nf
        self.__remote_host: str = remote_host
        self.__cNRF_AMF: str = cNRF_AMF
        self.__cNRF: str = cNRF
        self.__host:str = host
        self.__dn: str = dn
        self.__ns: str = ns
        self.__ip: str = ip
        self.__ver: int = int(ver)
        self.__region: str = region
        self.__del_flg: int = int(del_flg)


    @property
    def nf(self) -> str:
        """コマンド実行対象ホスト名プロパティ

        インスタンス属性のコマンド実行対象ホスト名を取得する

        Returns:
            str: インスタンス属性のコマンド実行対象ホスト名
        """
        return self.__nf

    @property
    def remote_host(self) -> str:
        """SSH接続ホスト名プロパティ

        インスタンス属性のSSH接続ホスト名を取得する

        Returns:
            str: インスタンス属性のSSH接続ホスト名
        """
        return self.__remote_host

    @property
    def cNRF_AMF(self) -> str:
        """

        """
        return self.__cNRF_AMF

    @property
    def cNRF(self) -> str:
        """
        
        """
        return self.__cNRF

    @property
    def host(self) -> str:
        """
        
        """
        return self.__host

    @property
    def dn(self) -> str:
        """プロパティ

        インスタンス属性のを取得する

        Returns:
            str: インスタンス属性の
        """
        return self.__dn


    @property
    def ns(self) -> str:
        """プロパティ

        インスタンス属性のを取得する

        Returns:
            str: インスタンス属性の
        """
        return self.__ns


    @property
    def ip(self) -> str:
        """接続先IPプロパティ

        インスタンス属性の接続先IPを取得する

        Returns:
            str: インスタンス属性の接続先IP
        """
        return self.__ip


    @property
    def ver(self) -> int:
        """プロパティ

        インスタンス属性のを取得する

        Returns:
            bool: インスタンス属性の
        """
        return self.__ver


    @property
    def region(self) -> str:
        """実行地域プロパティ

        インスタンス属性の実行地域を取得する

        Returns:
            bool: インスタンス属性の実行地域
        """
        return self.__region


    @property
    def del_flg(self) -> int:
        """プロパティ

        インスタンス属性のを取得する

        Returns:
            int: インスタンス属性の
        """
        return self.__del_flg

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
