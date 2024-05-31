import re
import pandas as pd
import pandas.core.series
import openpyxl
from typing import List, Dict, Any


class CommandConfig:
    """実行コマンド設定情報

    実行するコマンドの設定を保持する

    """

    def __init__(self, node: str, no: str, task: str, item: str, when: str, command: str, var: str, check_kind: str, result_OK: str, result_NG: str, option: str):
        """初期化

        Args:
            node (str): 実行環境名 コマンド実行する環境
            no(str): コマンド概要採番 実行するコマンド概要項目の採番
            task(str): コマンド概要要素 実行するコマンド概要項目の要素
            item (str): コマンド概要 実行するコマンドの概要項目
            when (str): 実行条件項目 コマンドを実行する条件の項目 
            command (str): コマンド名 実行するコマンド   
            var(str): コマンド実行元 コマンド実行元の変数名        
            check_kind (str): 確認条件項目 result_OK/result_NGで確認する条件
            result_OK (str): 正常結果判定項目 コマンド実行結果と比較して正常と判定される項目名
            result_NG (str): 異常結果判定項目 コマンド実行結果と比較して異常と判定される項目名
            option (str): 後続処理判定項目 エラー時、後続処理を停止するか判定する項目 disableである場合は後続処理を停止せずに実行、
                          ableの場合は後続処理を停止させる
        """
        self.__node: str = node
        self.__no: str = no
        self.__task: str = task
        self.__item: str = item
        self.__when: str = when
        self.__command: str = command
        self.__var: str = var
        self.__check_kind: str = check_kind
        self.__result_OK: str = result_OK
        self.__result_NG: str = result_NG
        self.__option: str = option

    @property
    def node(self) -> str:
        """実行環境名プロパティ

        インスタンス属性の実行環境を取得する

        Returns:
            str: インスタンス属性の実行環境
        """
        return self.__node

    @property
    def no(self) -> str:
        """実行採番プロパティ

        インスタンス属性の実行採番を取得する

        Returns:
            str: インスタンス属性の実行採番
        """
        return self.__no

    @property
    def task(self) -> str:
        """xxxxプロパティ

        インスタンス属性のxxxxを取得する

        Returns:
            str: インスタンス属性のxxxx
        """
        return self.__task

    @property
    def item(self) -> str:
        """コマンド概要項目情報プロパティ

        インスタンス属性のコマンド概要項目を取得する

        Returns:
            str: インスタンス属性のコマンド概要項目
        """
        return self.__item

    @property
    def when(self) -> str:
        """実行条件項目プロパティ

        インスタンス属性の実行条件項目を取得する

        Returns:
            str: インスタンス属性の実行条件項目
        """
        return self.__when

    @property
    def command(self) -> str:
        """コマンドプロパティ

        インスタンス属性のコマンドを取得する

        Returns:
            str: インスタンス属性のコマンド
        """
        return self.__command

    @property
    def var(self) -> str:
        """コマンド実行元プロパティ

        インスタンス属性のコマンド実行元を取得する

        Returns:
            str: インスタンス属性のコマンド実行元
        """
        return self.__var

    @property
    def check_kind(self) -> str:
        """確認条件項網プロパティ

        インスタンス属性の確認条件項目を取得する

        Returns:
            str: インスタンス属性の確認条件項目
        """
        return self.__check_kind

    @property
    def result_OK(self) -> str:
        """正常結果判定項目プロパティ

        インスタンス属性の正常結果判定項目を取得する

        Returns:
            str: インスタンス属性の正常結果判定項目
        """
        return self.__result_OK

    @property
    def result_NG(self) -> str:
        """異常結果判定項目プロパティ

        インスタンス属性の異常結果判定項目を取得する

        Returns:
            str: インスタンス属性の異常結果判定項目
        """
        return self.__result_NG

    @property
    def option(self) -> str:
        """後続処理判定項目プロパティ

        インスタンス属性の後続処理判定項目を取得する

        Returns:
            str: インスタンス属性の後続処理判定項目
        """
        return self.__option

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

