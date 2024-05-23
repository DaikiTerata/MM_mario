import re
import pandas as pd
import pandas.core.series
import openpyxl
from typing import List, Dict, Any

class MainConfig:
    """初期設定情報

    シナリオファイル設定情報の初期設定値を保持する

    """

    def __init__(self, key: str, value) -> None:
        """初期化

        Args:
            key (str): 初期値項目名 初期値に設定する項目名
            value: 初期設定値 初期値項目名に設定する値  数字であればint型、英数字と英字であればstr型で格納

        """
        self.__key: str = key
        self.__value = value


    @property
    def key(self) -> str:
        """初期値項目名プロパティ

        インスタンス属性の初期値項目名を取得する

        Returns:
            str: インスタンス属性の初期値項目名
        """
        return self.__key

    @property
    def value(self):
        """初期設定値プロパティ

        インスタンス属性の初期設定値を取得する

        Returns:
            str: インスタンス属性の初期設定値
        """
        return self.__value

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