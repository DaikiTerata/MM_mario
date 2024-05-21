"""ホスト設定情報

ホスト設定情報エクセルファイルを読み込み、読み込んだ情報を提供する

"""

import pandas as pd
import pandas.core.series
import openpyxl
from typing import List, Dict, Any


class AsciiFilter:
    """ASCIIフィルタ

    PANDASのSeries（読み込んだExcelファイルの行）が文字列の場合、文字列をASCIIコードのみとし、他のコードを削除してインスタンス属性に保持する
    文字列以外の場合はそのまま保持する
    """

    def __init__(self, row: pandas.core.series.Series) -> None:
        """初期化

        PANDASのSeries（読み込んだExcelファイルの行）が文字列の場合、文字列をASCIIコードのみとし、他のコードを削除してインスタンス属性に保持する
        文字列以外の場合はそのまま保持する
        """
        for col_name in row.index:
            setattr(self, col_name, AsciiFilter.__strip_to_ascii(row[col_name]))

    def __strip_to_ascii(org: Any) -> Any:
        """ASCIIコード以外削除

        引数が文字列の場合、文字列をASCIIコードのみとし、他のコードを削除して返却する
        文字列以外の場合はそのまま返却する

        Args:
            org (Any): 元データ

        Returns:
            Any: ASCIIコード以外削除データ（文字列以外の場合は元データ）
        """
        if org and type(org) == str:
            # No-Break SpaceをSpaceに変換しascii以外の文字コードを除去
            return org.replace('\u00a0', '\u0020').encode('ascii', 'ignore').decode('utf-8')
        return org

class NoteConfig:
    """備考メモ情報

    備考情報を保持する

    """

    def __init__(self, note: str):
        """初期化

        引数で受け取った情報をインスタンス属性に設定する

        Args:
            note (str): 備考項目 メモ項目

        Raises:
            
        """
        self.__note: str = note

    @property
    def note(self) -> str:
        """備考項目プロパティ

        インスタンス属性の備考項目を取得する

        Returns:
            str: インスタンス属性の備考項目
        """
        return self.__note

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

class OptionConfig:
    """後続処理判定設定情報

    後続処理判定項目、備考項目を保持する

    """

    def __init__(self, option: str, noteConfigs: Dict[str, NoteConfig]):
        """初期化

        引数で受け取った情報をインスタンス属性に設定する

        Args:
            option (str): 後続処理判定項目 エラー時、後続処理を停止するか判定する項目 disableである場合は後続処理を停止せずに実行、ableの場合は後続処理を停止させる
            noteConfigs(noteConfigs: Dict[str, NoteConfig]): 備考情報

        Raises:
            
        """
        self.__option: str = option
        self.__noteConfigs: Dict[str, NoteConfig] = noteConfigs

    @property
    def option(self) -> str:
        """後続処理判定項目プロパティ

        インスタンス属性の後続処理判定項目を取得する

        Returns:
            str: インスタンス属性の後続処理判定項目
        """
        return self.__option

    @property
    def noteConfigs(self) -> Dict[str, NoteConfig]:
        """備考項目プロパティ

        インスタンス属性の備考情報を取得する

        Returns:
            Dict[str, NoteConfigs]: インスタンス属性の備考情報
        """
        return self.__noteConfigs

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


class NGResultConfig:
    """異常結果設定情報

    異常結果判定項目を保持する

    """

    def __init__(self, result_NG: str, optionConfigs: Dict[str, OptionConfig]):
        """初期化

        引数で受け取った情報をインスタンス属性に設定する

        Args:
            result_NG (str): 異常結果判定項目 コマンド実行結果と比較して異常と判定される項目名
            optionConfigs (Dict[str, OptionConfig]): 後続処理判定設定情報
            boolにするか？

        Raises:
            
        """
        self.__result_NG: str = result_NG
        self.__optionConfigs: Dict[str, OptionConfig] = optionConfigs

    @property
    def result_NG(self) -> str:
        """異常結果判定項目プロパティ

        インスタンス属性の異常結果判定項目を取得する

        Returns:
            str: インスタンス属性の異常結果判定項目
        """
        return self.__result_NG

    @property
    def optionConfigs(self) -> Dict[str, OptionConfig]:
        """後続処理判定設定情報プロパティ

        インスタンス属性の後続処理判定設定情報を取得する

        Returns:
            Dict[str, OptionConfig]: インスタンス属性の後続処理判定設定情報
        """
        return self.__optionConfigs

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


class OKResultConfig:
    """正常結果設定情報

    正常結果判定項目を保持する

    """

    def __init__(self, result_OK: str, ngresultConfigs: Dict[str, NGResultConfig]):
        """初期化

        引数で受け取った情報をインスタンス属性に設定する

        Args:
            result_OK (str): 正常結果判定項目 コマンド実行結果と比較して正常と判定される項目名
            ngresultConfigs (Dict[str, NGResultConfig]): 異常結果設定情報 コマンド実行結果と比較して異常と判定される情報
            boolにするか？

        Raises:
            
        """
        self.__result_OK: str = result_OK
        self.__ngresultConfigs: Dict[str, NGResultConfig] = ngresultConfigs

    @property
    def result_OK(self) -> str:
        """正常結果判定項目プロパティ

        インスタンス属性の正常結果判定項目を取得する

        Returns:
            str: インスタンス属性の正常結果判定項目
        """
        return self.__result_OK

    @property
    def ngresultConfigs(self) -> Dict[str, NGResultConfig]:
        """異常結果設定情報プロパティ

        インスタンス属性の異常結果設定情報を取得する

        Returns:
            Dict[str, NGResultConfig]: インスタンス属性の異常結果設定情報
        """
        return self.__ngresultConfigs

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


class CheckKindConfig:
    """確認条件設定情報

    確認条件の設定を保持する。

    """

    def __init__(self, check_kind: str, okresultConfigs: Dict[str, OKResultConfig]):
        """初期化

        引数で受け取った情報をインスタンス属性に設定する

        Args:
            check_kind (str): 確認条件項目 result_OK/result_NGで確認する条件
            okresultConfigs (): 正常結果設定情報 コマンド実行結果と比較して正常と判定される情報
        """
        self.__check_kind: str = check_kind
        self.__okresultConfigs: Dict[str, OKResultConfig] = okresultConfigs

    @property
    def check_kind(self) -> str:
        """確認条件項網プロパティ

        インスタンス属性の確認条件項目を取得する

        Returns:
            str: インスタンス属性の確認条件項目
        """
        return self.__check_kind

    @property
    def okresultConfigs(self) -> Dict[str, OKResultConfig]:
        """正常結果設定情報プロパティ

        インスタンス属性の正常結果設定情報を取得する

        Returns:
            Dict[str, OKResultConfig]: インスタンス属性の正常結果設定情報
        """
        return self.__okresultConfigs

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


class WhenConfig:
    """実行条件設定情報

    コマンドを実行する条件の設定を保持する

    """

    def __init__(self, when: str, checkkindConfigs: Dict[str, CheckKindConfig]):
        """初期化

        引数で受け取った情報をインスタンス属性に設定する

        Args:
            when (str): 実行条件項目 コマンドを実行する条件の項目
            checkkindConfigs (Dict[str, CheckKindConfig]): 確認条件設定情報
        """
        self.__when: str = when
        self.__checkkindConfigs: Dict[str, CheckKindConfig] = checkkindConfigs

    @property
    def when(self) -> str:
        """実行条件項目プロパティ

        インスタンス属性の実行条件項目を取得する

        Returns:
            str: インスタンス属性の実行条件項目
        """
        return self.__when

    @property
    def checkkindConfigs(self) -> Dict[str, CheckKindConfig]:
        """実行条件設定情報プロパティ

        インスタンス属性の実行条件設定情報を取得する

        Returns:
            Dict[str, CheckKindConfig]: インスタンス属性の実行条件設定情報
        """
        return self.__checkkindConfigs

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


class CommandConfig:
    """コマンド設定情報

    実行するコマンドの情報を保持する

    """

    def __init__(self, command: str, whenConfigs: Dict[str, WhenConfig]):
        """初期化

        Args:
            command (str): コマンド 実行するコマンド
            whenConfigs (Dict[str, WhenConfig]): 実行条件設定情報
        """
        self.__command: str = command
        self.__whenConfigs: Dict[str, WhenConfig] = whenConfigs

    @property
    def command(self) -> str:
        """コマンドプロパティ

        インスタンス属性のコマンドを取得する

        Returns:
            str: インスタンス属性のコマンド
        """
        return self.__command

    @property
    def whenConfigs(self) -> Dict[str, WhenConfig]:
        """実行条件設定情報プロパティ

        インスタンス属性の実行条件設定情報を取得する

        Returns:
            Dict[str, WhenConfig]: インスタンス属性の実行条件設定情報
        """
        return self.__whenConfigs

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


class ItemConfig:
    """コマンド概要設定情報

    実行するコマンドの概要を示した設定を保持する

    """

    def __init__(self, item: str, commandConfigs: Dict[str, CommandConfig]):
        """初期化

        Args:
            item (str): コマンド概要項目 実行するコマンドの概要
            commandConfigs (Dict[str, CommandConfig]): コマンド設定情報
        """
        self.__item: str = item
        self.__commandConfigs: Dict[str, CommandConfig] = commandConfigs

    @property
    def item(self) -> str:
        """コマンド概要項目プロパティ

        インスタンス属性のコマンド概要項目を取得する

        Returns:
            str: インスタンス属性のコマンド概要項目
        """
        return self.__item

    @property
    def commandConfigs(self) -> Dict[str, CommandConfig]:
        """コマンド設定情報プロパティ

        インスタンス属性のコマンド設定情報を取得する

        Returns:
            Dict[str, CommandConfig]: インスタンス属性のコマンド設定情報
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


class NodeConfig:
    """実行環境設定情報

    コマンド実行する環境の設定を保持する

    """

    def __init__(self, node: str, itemConfigs: Dict[str, ItemConfig]):
        """初期化

        Args:
            node (str): 実行環境名 コマンド実行する環境
            itemConfigs (Dict[str, ItemConfig]): コマンド概要設定情報
        """
        self.__node: str = node
        self.__itemConfigs: Dict[str, ItemConfig] = itemConfigs

    @property
    def node(self) -> str:
        """実行環境名プロパティ

        インスタンス属性の実行環境を取得する

        Returns:
            str: インスタンス属性の実行環境
        """
        return self.__node

    @property
    def itemConfigs(self) -> Dict[str, ItemConfig]:
        """コマンド概要設定情報プロパティ

        インスタンス属性のコマンド概要設定情報を取得する

        Returns:
            Dict[str, ItemConfig]: インスタンス属性のコマンド概要設定情報
        """
        return self.__itemConfigs

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


class ScenarioConfig:
    """シナリオ設定情報

    シナリオの設定を保持する

    """

    def __init__(self, scenario: str, nodeConfigs: Dict[str, NodeConfig]):
        """初期化

        Args:
            scenario (str): シナリオ名 ツール実行を行うシナリオ名
            nodeConfigs (Dict[str, NodeConfig]): 実行環境設定情報
        """
        self.__scenario: str = scenario
        self.__nodeConfigs: Dict[str, NodeConfig] = nodeConfigs

    @property
    def scenario(self) -> str:
        """シナリオ名プロパティ

        インスタンス属性のシナリオ名を取得する

        Returns:
            str: インスタンス属性のシナリオ名
        """
        return self.__scenario

    @property
    def nodeConfigs(self) -> Dict[str, NodeConfig]:
        """実行環境設定情報プロパティ

        インスタンス属性の実行環境設定情報を取得する

        Returns:
            Dict[str, NodeConfig]: インスタンス属性の実行環境設定情報
        """
        return self.__nodeConfigs

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


class AccessHostConfig:
    """接続ホスト設定情報

    SSH接続のための設定を保持する

    """

    def __init__(self, access_host: str, nf_ip: str, nf_auth_method: int, nf_user: str, nf_password: str, nf_key_info: str,
                 priority: int, bastion: int) -> None:
        """初期化

        Args:
            access_host (str): 接続先ホスト名
            nf_ip (str): 接続先IPアドレス
            nf_auth_method (int): 認証方式 1: ID/PW認証 2:公開鍵認証
            nf_user (str): ユーザ 接続用ユーザID
            nf_password (str): パスワード 接続用パスワード
            nf_key_info (str): 鍵情報 鍵配置先情報
            priority (int): 優先順位 数値の小さい（プライオリティの高い）ホストから順に接続し、接続できたホストでコマンドを実行する
            bastion (int): 多段接続 数値の小さい（接続段数の少ない）ホストに接続し、そのホストから次のホストに接続する　最後のホストでコマンドを実行する

        Raises:
            ValueError: nf_auth_methodが1、2以外の場合、priority,bastionをintに変換できない場合に発生
        """
        self.__access_host: str = access_host
        self.__nf_ip: str = nf_ip
        nf_auth_method = int(nf_auth_method)
        if nf_auth_method != 1 and nf_auth_method != 2:
            raise ValueError(f"nf_auth_method must be {{1|2}}. value:{nf_auth_method}")
        self.__nf_auth_method: int = nf_auth_method
        self.__nf_user: str = nf_user
        self.__nf_password: str = nf_password
        self.__nf_key_info: str = nf_key_info
        self.__priority: int = int(priority)
        self.__bastion: int = int(bastion)

    @property
    def access_host(self) -> str:
        """接続先ホスト名プロパティ

        インスタンス属性の接続先ホスト名を取得する

        Returns:
            str: インスタンス属性の接続先ホスト名
        """
        return self.__access_host

    @property
    def nf_ip(self) -> str:
        """接続先IPアドレスプロパティ

        インスタンス属性の接続先IPアドレスを取得する

        Returns:
            str: インスタンス属性の接続先IPアドレス
        """
        return self.__nf_ip

    @property
    def nf_auth_method(self) -> int:
        """認証方式プロパティ

        インスタンス属性の認証方式を取得する

        Returns:
            int: インスタンス属性の認証方式 1: ID/PW認証 2:公開鍵認証
        """
        return self.__nf_auth_method

    @property
    def nf_user(self) -> str:
        """ユーザプロパティ

        インスタンス属性のユーザを取得する

        Returns:
            str: インスタンス属性のユーザ
        """
        return self.__nf_user

    @property
    def nf_password(self) -> str:
        """パスワードプロパティ

        インスタンス属性のパスワードを取得する

        Returns:
            str: インスタンス属性のパスワード
        """
        return self.__nf_password

    @property
    def nf_key_info(self) -> str:
        """鍵情報プロパティ

        インスタンス属性の鍵情報を取得する

        Returns:
            str: インスタンス属性の鍵情報
        """
        return self.__nf_key_info

    @property
    def priority(self) -> int:
        """優先順位プロパティ

        インスタンス属性の優先順位を取得する

        Returns:
            int: インスタンス属性の優先順位
        """
        return self.__priority

    @property
    def bastion(self) -> int:
        """多段接続プロパティ

        インスタンス属性の多段接続を取得する

        Returns:
            int: インスタンス属性の多段接続
        """
        return self.__bastion

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


class ConnectConfig:
    """接続設定情報

    コマンド収集ホストへの接続のための設定を保持する

    """

    def __init__(self, nf_host: str, vendor: str, nf_type: str, enable_flag: bool, close_flag: bool, accessHostConfigs: List[AccessHostConfig]) -> None:
        """初期化

        Args:
            nf_host (str): コマンド収集ホスト名 コマンドを実行し情報を収集するホスト名
            vendor (str): ベンダー名 ホストのベンダー
            nf_type (str): NF種別 ホストのNF種別
            enable_flag (bool): 有効化フラグ 収集を実行するかの可否フラグ true:実行する false:実行しない
            close_flag (bool): 切断フラグ コマンド実行後接続終了要否フラグ true:切断する false:切断しない
            accessHostConfigs (List[AccessHostConfig]): 接続ホスト設定情報

        """
        self.__nf_host: str = nf_host
        self.__vendor: str = vendor
        self.__nf_type: str = nf_type
        self.__enable_flag: bool = bool(enable_flag)
        self.__close_flag: bool = bool(close_flag)
        self.__accessHostConfigs: List[AccessHostConfig] = accessHostConfigs

    @property
    def nf_host(self) -> str:
        """コマンド収集ホスト名プロパティ

        インスタンス属性のコマンド収集ホスト名を取得する

        Returns:
            str: インスタンス属性のコマンド収集ホスト名
        """
        return self.__nf_host

    @property
    def vendor(self) -> str:
        """ベンダー名プロパティ

        インスタンス属性のベンダー名を取得する

        Returns:
            str: インスタンス属性のベンダー名
        """
        return self.__vendor

    @property
    def nf_type(self) -> str:
        """NF種別プロパティ

        インスタンス属性のNF種別を取得する

        Returns:
            str: インスタンス属性のNF種別
        """
        return self.__nf_type

    @property
    def enable_flag(self) -> bool:
        """有効化フラグプロパティ

        インスタンス属性の有効化フラグを取得する

        Returns:
            str: インスタンス属性の有効化フラグ
        """
        return self.__enable_flag

    @property
    def close_flag(self) -> bool:
        """切断フラグ

        インスタンス属性の切断フラグを取得する

        Returns:
            bool: インスタンス属性の切断フラグ
        """
        return self.__close_flag

    @property
    def accessHostConfigs(self) -> List[AccessHostConfig]:
        """接続ホスト設定情報プロパティ

        インスタンス属性の接続ホスト設定情報を取得する

        Returns:
            str: インスタンス属性の接続ホスト設定情報
        """
        return self.__accessHostConfigs

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


class Config:
    """設定情報

    シナリオ設定情報ファイルを読み込み、ファイルに設定されたメイン処理設定情報、接続設定情報、サブ処理設定情報を保持する

    """

    def __init__(self, config_file_name: str):
        """初期化

        引数で指定されたシナリオ設定情報ファイルを読み込み、インスタンス属性に保持する

        Args:
            config_file_name (str): シナリオ設定情報ファイルパス
        """
        config_file = pd.ExcelFile(config_file_name, engine='openpyxl')
        self.__mainConfigs: Dict[str, ScenarioConfig] = Config.__load_main_process_info(config_file)
        # self.__subConfigs: Dict[str, ScenarioConfig] = Config.__load_sub_process_info(config_file)
        # self.__connectConfigs: List[ConnectConfig] = Config.__load_connect_info(config_file)
        # self.__moConfigs: Dict[str, MoConfig] = Config.__load_collect_info(config_file)
        # self.__cmdHostConfigs: Dict[str, CmdHostConfig] = Config.__load_nf_host_info(self.__moConfigs)
        # self.__connectConfigs: List[ConnectConfig] = Config.__load_connect_info(config_file)

    @property
    def mainConfigs(self) -> Dict[str, ScenarioConfig]:
        """メイン設定情報プロパティ

        インスタンス属性のメイン設定情報を取得する

        Returns:
            Dict[str, ScenarioConfig]: メイン設定情報
        """
        return self.__mainConfigs

    # @property
    # def connectConfigs(self) -> List[ConnectConfig]:
    #     """接続設定情報プロパティ

    #     インスタンス属性の接続設定情報を取得する

    #     Returns:
    #         List[ConnectConfig]: 接続設定情報
    #     """
    #     return self.__connectConfigs

    # @property
    # def subConfigs(self) -> Dict[str, ScenarioConfig]:
    #     """サブ設定情報プロパティ

    #     インスタンス属性のサブ設定情報を取得する

    #     Returns:
    #         Dict[str, ScenarioConfig]: サブ設定情報
    #     """
    #     return self.__subConfigs

    def __load_main_process_info(config_file: pd.ExcelFile) -> Dict[str, ScenarioConfig]:
        """メイン設定情報ロード

        シナリオ設定情報ファイルの「MAIN」シートから情報を読み込み、メイン設定情報として返却する

        Args:
            config_file (pd.ExcelFile): ホスト設定情報ファイル（pandasでExcelファイルを表すクラスのオブジェクト）

        Returns:
            Dict[str, ScenarioConfig]: メイン設定情報 キーはシナリオ名
        """
        # 設定情報ファイルから「MAIN」シートの情報を読み込む
        collect_sheet = config_file.parse('MAIN')
        # シナリオ設定情報辞書を初期化する
        scenarioConfigs: Dict[str, ScenarioConfig] = {}
        # 実行環境設定情報辞書を初期化する
        nodeConfigs: Dict[str, NodeConfig] = {}
        # コマンド概要設定情報辞書を初期化する
        itemConfigs: Dict[str, ItemConfig] = {}
        # コマンド設定情報辞書を初期化する
        commandConfigs: Dict[str, CommandConfig] = {}
        # 実行条件設定情報辞書を初期化する
        whenConfigs: Dict[str, WhenConfig] = {}
        # 確認条件設定情報辞書を初期化する
        checkkindConfigs: Dict[str, CheckKindConfig] = {}
        # 正常結果設定情報辞書を初期化する
        okresultConfigs: Dict[str, OKResultConfig] = {}
        # 異常結果設定情報辞書を初期化する
        ngresultConfigs: Dict[str, NGResultConfig] = {}
        # 後続処理判定設定情報辞書を初期化する
        optionConfigs: Dict[str, OptionConfig] = {}
        # 備考メモ情報辞書を初期化する
        noteConfigs: Dict[str, NoteConfig] = {}
        # MAINシートの行でループする
        for row in [AsciiFilter(row) for _, row in collect_sheet.iterrows()]:
            # MAINシートの行のシナリオ名がnullでない場合
            if not pd.isnull(row.scenario):
                # 実行環境設定情報辞書を初期化する
                nodeConfigs: Dict[str, NodeConfig] = {}
                # シナリオ設定情報をMAINシートの行の情報と実行環境設定情報辞書で生成し、シナリオ設定情報辞書にシナリオ名をキーとして追加する
                scenarioConfigs[row.scenario] = ScenarioConfig(row.scenario, nodeConfigs)

            # MAINシートの行の実行環境名がnullでない場合
            if not pd.isnull(row.node):
                # コマンド概要設定情報辞書を初期化する
                itemConfigs: Dict[str, ItemConfig] = {}
                # 実行環境設定情報をMAINシートの行の情報とコマンド概要設定情報辞書で生成し、実行環境設定情報辞書に実行環境名をキーとして追加する
                nodeConfigs[row.node] = NodeConfig(row.node, itemConfigs)

            # MAINシートの行の実行環境名がnullでない場合
            if not pd.isnull(row.item):
                # コマンド設定情報辞書を初期化する
                commandConfigs: Dict[str, CommandConfig] = {}
                # コマンド概要設定情報をMAINシートの行の情報とコマンド設定情報辞書で生成し、コマンド概要設定情報辞書にコマンド概要項目をキーとして追加する
                itemConfigs[row.item] = ItemConfig(row.item, commandConfigs)

            # MAINシートの行の実行環境名がnullでない場合
            if not pd.isnull(row.command):
                # 実行条件設定情報辞書を初期化する
                whenConfigs: Dict[str, WhenConfig] = {}
                # コマンド設定情報をMAINシートの行の情報と実行条件設定情報辞書で生成し、コマンド設定情報辞書にコマンド名をキーとして追加する
                commandConfigs[row.command] = CommandConfig(row.command, whenConfigs)

            # MAINシートの行の実行環境名がnullでない場合
            if not pd.isnull(row.when):
                # 確認条件設定情報辞書を初期化する
                checkkindConfigs: Dict[str, CheckKindConfig] = {}
                # 実行条件設定情報をMAINシートの行の情報と確認条件設定情報辞書で生成し、実行条件設定情報辞書に実行条件項目をキーとして追加する
                whenConfigs[row.when] = WhenConfig(row.when, checkkindConfigs)

            # MAINシートの行の実行環境名がnullでない場合
            if not pd.isnull(row.check_kind):
                # 正常結果設定情報辞書を初期化する
                okresultConfigs: Dict[str, OKResultConfig] = {}
                # 確認条件設定情報をMAINシートの行の情報と正常結果設定情報辞書で生成し、確認条件設定情報辞書に確認条件項目をキーとして追加する
                checkkindConfigs[row.check_kind] = CheckKindConfig(row.check_kind, okresultConfigs)

            # MAINシートの行の実行環境名がnullでない場合
            if not pd.isnull(row.result_OK):
                # 異常結果設定情報辞書を初期化する
                ngresultConfigs: Dict[str, NGResultConfig] = {}
                # 正常結果設定情報をMAINシートの行の情報と異常結果設定情報辞書で生成し、正常結果設定情報辞書に正常結果項目をキーとして追加する
                okresultConfigs[row.result_OK] = OKResultConfig(row.result_OK, ngresultConfigs)

            # MAINシートの行の実行環境名がnullでない場合
            if not pd.isnull(row.result_NG):
                # 後続処理判定設定情報辞書を初期化する
                optionConfigs: Dict[str, OptionConfig] = {}
                # 異常結果設定情報をMAINシートの行の情報と後続処理判定設定情報辞書で生成し、異常結果設定情報辞書に異常結果項目をキーとして追加する
                ngresultConfigs[row.result_NG] = NGResultConfig(row.result_NG, optionConfigs)

                # 備考メモ情報辞書を初期化する
                noteConfigs: Dict[str, NoteConfig] = {}
                # 後続処理判定設定情報をMAINシートの行の情報と備考メモ情報辞書で生成し、後続処理判定設定情報辞書に後続処理判定項目をキーとして追加する
                optionConfigs[row.option] = OptionConfig(row.option, noteConfigs)

                # 備考メモ情報をMAINシートの行の情報で生成し、備考メモ情報辞書に備考メモ項目をキーとして追加する
                noteConfigs[row.note] = NoteConfig(row.note)

        # 収集設定情報辞書を返却する
        return scenarioConfigs

    # def __load_nf_host_info(moConfigs: Dict[str, MoConfig]) -> Dict[str, CmdHostConfig]:
    #     """コマンド収集ホスト設定情報ロード

    #     収集設定情報からコマンド収集ホスト単位に情報を集約し、コマンド収集ホスト設定情報として返却する

    #     Args:
    #         moConfigs (Dict[str, MoConfig]): 収集設定情報

    #     Returns:
    #         Dict[str, CmdHostConfig]: コマンド収集ホスト設定情報
    #     """
    #     # コマンド収集ホスト設定情報辞書を初期化する
    #     cmdHostDict: Dict[str, CmdHostConfig] = {}
    #     # 引数の収集設定情報の項目でループする
    #     for moConfigTpl in moConfigs.items():
    #         # 収集設定情報の収集単位設定情報の項目でループする
    #         for unitConfigTpl in moConfigTpl[1].unitConfigs.items():
    #             # 収集単位設定情報のコマンド収集ホスト設定情報の項目でループする
    #             for cmdHostConfigTpl in unitConfigTpl[1].cmdHostConfigs.items():
    #                 # コマンド収集ホスト設定情報のコマンド収集ホスト名がコマンド収集ホスト設定情報辞書に登録されていない場合
    #                 if cmdHostConfigTpl[0] not in cmdHostDict:
    #                     # コマンド収集ホスト設定情報の情報から登録用コマンド収集ホスト設定情報を生成し、コマンド収集ホスト設定情報辞書に登録する（コマンド設定情報は空で生成する）
    #                     cmdHostDict[cmdHostConfigTpl[0]] = CmdHostConfig(cmdHostConfigTpl[0], {})
    #                 # コマンド収集ホスト設定情報辞書に登録されているコマンド収集ホスト設定情報を登録コマンド収集ホスト設定情報として取得する
    #                 cmdHost = cmdHostDict.get(cmdHostConfigTpl[0])
    #                 # コマンド収集ホスト設定情報のコマンド設定情報の項目でループする
    #                 for cmdConfigTpl in cmdHostConfigTpl[1].cmdConfigs.items():
    #                     # コマンド設定情報のコマンド名が登録コマンド収集ホスト設定情報のコマンド設定情報に登録されていない場合
    #                     if cmdConfigTpl[0] not in cmdHost.cmdConfigs:
    #                         # コマンド設定情報を生成し、登録コマンド収集ホスト設定情報のコマンド設定情報に登録する（カウンタ設定情報は空で生成する）
    #                         cmdHost.cmdConfigs[cmdConfigTpl[0]] = CmdConfig(cmdConfigTpl[0], {})
    #                     # 登録コマンド収集ホスト設定情報のコマンド設定情報に登録されているコマンド設定情報を登録コマンド設定情報として取得する
    #                     cmd = cmdHost.cmdConfigs.get(cmdConfigTpl[0])
    #                     # 引数の収集設定情報.収集単位設定情報.コマンド収集ホスト設定情報.コマンド設定情報のカウンタ設定情報の項目でループする
    #                     for counterConfigTpl in cmdConfigTpl[1].counterConfigs.items():
    #                         # 引数の収集設定情報.収集単位設定情報.コマンド収集ホスト設定情報.コマンド設定情報.カウンタ設定情報の結果カウンタ名が登録コマンド設定情報のカウンタ設定情報に登録されていない場合
    #                         if cmdConfigTpl[0] not in cmd.counterConfigs:
    #                             # カウンタ設定情報を生成し、登録コマンド設定情報のカウンタ設定情報に登録する
    #                             cmd.counterConfigs[counterConfigTpl[0]] = CounterConfig(
    #                                 counterConfigTpl[1].cmd_count_item, counterConfigTpl[1].counter_name, None)
    #     # コマンド収集ホスト設定情報辞書を返却する
    #     return cmdHostDict

    # def __load_connect_info(config_file: pd.ExcelFile) -> List[ConnectConfig]:
    #     """接続設定情報ロード

    #     設定情報ファイルの「接続情報」シートから情報を読み込み、接続設定情報として返却する
    #     収集ホスト設定情報配下の接続設定情報はpriority、bastionの昇順でソートされる

    #     Args:
    #         config_file (pd.ExcelFile): ホスト設定情報ファイル（pandasでExcelファイルを表すオブジェクト）

    #     Returns:
    #         List[ConnectConfig]: 接続設定情報
    #     """
    #     # 設定情報ファイルから「接続情報」シートの情報を読み込む
    #     connect_sheet = config_file.parse('接続情報')
    #     # 接続設定情報リストを初期化する
    #     connectConfigs: List[ConnectConfig] = []
    #     # 接続情報シートの行でループする
    #     for row in [AsciiFilter(row) for _, row in connect_sheet.iterrows()]:
    #         # 接続情報シートの行のコマンド収集ホスト名がnullでない場合
    #         if not pd.isnull(row.nf_host):
    #             # 接続ホスト設定情報リストを初期化する
    #             accessHostConfigs: List[AccessHostConfig] = []
    #             # 接続情報シートの行の情報と接続ホスト設定情報リストから接続設定情報を生成し、接続設定情報リストに追加する
    #             connectConfigs.append(
    #                 ConnectConfig(row.nf_host, row.vendor, row.nf_type, bool(row.enable_flag), bool(row.close_flag),
    #                               accessHostConfigs))
    #         # 接続情報シートの行の接続ホスト名がnullでない場合
    #         if not pd.isnull(row.access_host):
    #             # 接続情報シートの行の情報で接続ホスト設定情報を生成し、接続ホスト設定情報に追加する
    #             accessHostConfigs.append(
    #                 AccessHostConfig(row.access_host, row.nf_ip, int(row.nf_auth_method), row.nf_user, row.nf_password, row.nf_key_info,
    #                                  int(row.priority), int(row.bastion)))
    #     # 接続設定情報リストでループする
    #     for connectConfig in connectConfigs:
    #         # 接続設定情報の接続ホスト設定情報が２つ以上存在する場合
    #         if len(connectConfig.accessHostConfigs) >= 2:
    #             # 接続設定情報の接続ホスト設定情報を優先順位、多段接続の昇順でソートする
    #             bastion_digits: int = len(str(max([accessHostConfig.bastion for accessHostConfig in connectConfig.accessHostConfigs])))
    #             connectConfig.accessHostConfigs.sort(key=lambda x: x.priority*(10**bastion_digits) + x.bastion)
    #         else:
    #             pass
    #     return connectConfigs

    # def get_MoConfig_by_mo_host(self, mo_host: str) -> MoConfig:
    #     """収集設定情報取得

    #     指定されたOSS連携ホスト名に関連する収集設定情報を、保持している収集設定情報から取得する

    #     Args:
    #         mo_host (str): OSS連携ホスト名

    #     Returns:
    #         MoConfig: 指定されたOSS連携ホスト名に関連する収集設定情報
    #     """
    #     return self.__moConfigs.get(mo_host)

    # def get_ConnectConfig_by_nf_host(self, nf_host: str) -> ConnectConfig:
    #     """接続設定情報取得

    #     指定されたコマンド収集ホスト名に関連する接続設定情報を、保持している接続設定情報から取得する

    #     Args:
    #         nf_host (str): コマンド収集ホスト名

    #     Returns:
    #         ConnectConfig: 指定されたコマンド収集ホスト名に関連する接続設定情報
    #     """
    #     for connectConfig in self.__connectConfigs:
    #         if connectConfig.nf_host == nf_host:
    #             return connectConfig
    #     return None

    # def get_cmdHostConfig_by_nf_host(self, nf_host: str) -> CmdHostConfig:
    #     """コマンド収集ホスト設定情報取得

    #     指定されたコマンド収集ホスト名に関連するコマンド収集ホスト設定情報を保持しているコマンド収集ホスト設定情報から取得する

    #     Args:
    #         nf_host (str): コマンド収集ホスト名

    #     Returns:
    #         CmdHostConfig: コマンド収集ホスト設定情報
    #     """
    #     return self.__cmdHostConfigs.get(nf_host)


if __name__ == '__main__':
    config_file_name = 'C:\\prot_nf_auto\\bin\\MM_scenario_config.xlsx'
    config = Config(config_file_name)
    # 上手くシナリオ行が無い場合を継続的に読み込んでくれない
    # node以降の行を「command」としてひとくくりにし、再挑戦？
    # ↑なぜなら、node以降の行がまとめてループされるため
    print(config._Config__mainConfigs)