import re
import pandas as pd
import pandas.core.series
import openpyxl
from typing import List, Dict, Any
from MM_CommandConfig import CommandConfig

class ScenarioConfig:
    """シナリオ設定情報

    シナリオの設定を保持する

    """

    def __init__(self, scenario: str, commandConfigs: Dict[str, CommandConfig]):
        """初期化

        Args:
            scenario (str): シナリオ名 ツール実行を行うシナリオ名
            commandConfigs (Dict[str, CommandConfig]): 実行コマンド設定情報 キーは実行コマンド概要項目
        """
        self.__scenario: str = scenario
        self.__commandConfigs: Dict[str, CommandConfig] = commandConfigs

    @property
    def scenario(self) -> str:
        """シナリオ名プロパティ

        インスタンス属性のシナリオ名を取得する

        Returns:
            str: インスタンス属性のシナリオ名
        """
        return self.__scenario

    @property
    def commandConfigs(self) -> List[CommandConfig]:
        """実行コマンド設定情報プロパティ

        インスタンス属性の実行コマンド設定情報を取得する

        Returns:
            Dict[str, CommandConfig]: インスタンス属性の実行コマンド設定情報
        """
        return self.__commandConfigs

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
