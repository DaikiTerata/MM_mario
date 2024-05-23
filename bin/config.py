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


class CounterConfig:
    """カウンタ設定情報

    カウンタ名、集計タイプ（加算、減算）設定を保持する

    """

    def __init__(self, cmd_count_item: str, counter_name: str, aggregate_type: str):
        """初期化

        引数で受け取った情報をインスタンス属性に設定する

        Args:
            cmd_count_item (str): コマンドカウント項目 コマンドからカウンタ値を抽出する時に使用する項目
            counter_name (str): 結果カウンタ名 NF収集結果ファイルのカウンタ名として使用する名称
            aggregate_type (str): 集計タイプ カウンタ値を加算する場合add、減算する場合sub

        Raises:
            ValueError: aggregate_typeがadd、sub以外の場合に発生
        """
        self.__cmd_count_item: str = cmd_count_item
        self.__counter_name: str = counter_name
        aggregate_type = aggregate_type
        if aggregate_type and aggregate_type != 'add' and aggregate_type != 'sub':
            raise ValueError(f"aggregate_type must be {{'add'|'sub'}}. value:{aggregate_type}")
        self.__aggregate_type: str = aggregate_type

    @property
    def cmd_count_item(self) -> str:
        """コマンドカウント項目プロパティ

        インスタンス属性のコマンドカウント項目を取得する

        Returns:
            str: インスタンス属性のコマンドカウント項目
        """
        return self.__cmd_count_item

    @property
    def counter_name(self) -> str:
        """結果カウンタ名プロパティ

        インスタンス属性の結果カウンタ名を取得する

        Returns:
            str: インスタンス属性の結果カウンタ名
        """
        return self.__counter_name

    @property
    def aggregate_type(self) -> str:
        """集計タイププロパティ

        インスタンス属性の集計タイプを取得する

        Returns:
            str: インスタンス属性の集計タイプ
        """
        return self.__aggregate_type

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


class CmdConfig:
    """コマンド設定情報

    コマンド名、カウンタ設定情報の設定を保持する

    """

    def __init__(self, cmd: str, counterConfigs: Dict[str, CounterConfig]):
        """初期化

        引数で受け取った情報をインスタンス属性に設定する

        Args:
            counterConfigs (Dict[str, CounterConfig]): カウンタ設定情報 キーはCounterConfigの結果カウンタ名
        Args:
            cmd (str): コマンド名 実行するコマンド
            counterConfigs (): _description_
        """
        self.__cmd: str = cmd
        self.__counterConfigs: Dict[str, CounterConfig] = counterConfigs

    @property
    def cmd(self) -> str:
        """コマンド名プロパティ

        インスタンス属性のコマンド名を取得する

        Returns:
            str: インスタンス属性のコマンド名
        """
        return self.__cmd

    @property
    def counterConfigs(self) -> Dict[str, CounterConfig]:
        """カウンタ設定情報プロパティ

        インスタンス属性のカウンタ設定情報を取得する

        Returns:
            Dict[str, CounterConfig]: インスタンス属性のカウンタ設定情報
        """
        return self.__counterConfigs

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


class CmdHostConfig:
    """コマンド収集ホスト設定情報

    コマンド収集ホスト名、コマンド設定情報の設定を保持する

    """

    def __init__(self, nf_host: str, cmdConfigs: Dict[str, CmdConfig]):
        """初期化

        引数で受け取った情報をインスタンス属性に設定する

        Args:
            nf_host (str): コマンド収集ホスト名 コマンドを実行し情報を収集するホスト名
            cmdConfigs (Dict[str, CmdConfig]): コマンド設定情報 キーはCmdConfigのcmd
        """
        self.__nf_host: str = nf_host
        self.__cmdConfigs: Dict[str, CmdConfig] = cmdConfigs

    @property
    def nf_host(self) -> str:
        """コマンド収集ホスト名プロパティ

        インスタンス属性のコマンド収集ホスト名を取得する

        Returns:
            str: インスタンス属性のコマンド収集ホスト名
        """
        return self.__nf_host

    @property
    def cmdConfigs(self) -> Dict[str, CmdConfig]:
        """コマンド設定情報プロパティ

        インスタンス属性のコマンド設定情報を取得する

        Returns:
            Dict[str, CmdConfig]: インスタンス属性のコマンド設定情報
        """
        return self.__cmdConfigs

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


class UnitConfig:
    """集計単位設定情報

    集計単位毎の設定情報を保持する

    """

    def __init__(self, fixed_response_flag: bool, fixed_response_message: str,
                 unit: str, output_pattern: str, start_duration: int, end_duration: int, record_num: int,
                 required_record_percent: int, cmdHostConfigs: Dict[str, CmdHostConfig]) -> None:
        """初期化

        Args:
            fixed_response_flag (bool): 固定値返却フラグ 算出を行わず固定値を返却する場合true、算出を行う場合false
            fixed_response_message (str): 返却固定値 算出を行わず固定値を返却する場合の文字列　算出を行う場合は空
            unit (str): 単位 算出する値の単位
            output_pattern (str): 出力パターン名 指定可能なのは「A」および「B」のみ
            start_duration (int): 開始期間 情報取得期間の開始 指定時間から減算する時間 分単位
            end_duration (int): 終了期間 情報取得期間の終了 指定時間に加算する時間 分単位
            record_num (int): 情報数 情報取得期間に取得すべき情報数
            required_record_percent (int): 取得件数割合閾値 取得した情報の取得すべき情報に対する割合が許容される閾値 パーセント単位
            cmdHostConfigs (Dict[str, CmdHostConfig]): コマンド収集ホスト設定情報 キーはCmdHostConfigのnf_host

        Raises:
            ValueError: output_patternがA、B以外の場合に発生
        """
        self.__fixed_response_flag: bool = bool(fixed_response_flag)
        self.__fixed_response_message: str = fixed_response_message
        self.__unit: str = unit
        if (output_pattern
            and output_pattern != 'A'
            and output_pattern != 'B'
            and output_pattern != 'C'
                and output_pattern != 'D'):
            raise ValueError(f"aggregate_type must be {{A|B|C|D}}. value:{output_pattern}")
        self.__output_pattern: str = output_pattern
        self.__start_duration: int = int(start_duration)
        self.__end_duration: int = int(end_duration)
        self.__record_num: int = int(record_num)
        self.__required_record_percent: int = int(required_record_percent)
        self.__cmdHostConfigs: Dict[str, CmdHostConfig] = cmdHostConfigs

    @property
    def fixed_response_flag(self) -> bool:
        """固定値返却フラグプロパティ

        インスタンス属性の固定値返却フラグを取得する

        Returns:
            bool: インスタンス属性の固定値返却フラグ
        """
        return self.__fixed_response_flag

    @property
    def fixed_response_message(self) -> str:
        """返却固定値プロパティ

        インスタンス属性の返却固定値を取得する

        Returns:
            str: インスタンス属性の返却固定値
        """
        return self.__fixed_response_message

    @property
    def unit(self) -> str:
        """単位プロパティ

        インスタンス属性の単位を取得する

        Returns:
            str: インスタンス属性の単位
        """
        return self.__unit

    @property
    def output_pattern(self) -> str:
        """出力パターン名プロパティ

        インスタンス属性の出力パターン名を取得する

        Returns:
            str: インスタンス属性の出力パターン名
        """
        return self.__output_pattern

    @property
    def start_duration(self) -> int:
        """開始期間プロパティ

        インスタンス属性の開始期間を取得する

        Returns:
            int: インスタンス属性の開始期間
        """
        return self.__start_duration

    @property
    def end_duration(self) -> int:
        """終了期間プロパティ

        インスタンス属性の終了期間を取得する

        Returns:
            int: インスタンス属性の終了期間
        """
        return self.__end_duration

    @property
    def record_num(self) -> int:
        """情報数プロパティ

        インスタンス属性の情報数を取得する

        Returns:
            int: インスタンス属性の情報数
        """
        return self.__record_num

    @property
    def required_record_percent(self) -> int:
        """取得件数割合閾値プロパティ

        インスタンス属性の取得件数割合閾値を取得する

        Returns:
            int: インスタンス属性の取得件数割合閾値
        """
        return self.__required_record_percent

    @property
    def cmdHostConfigs(self) -> Dict[str, CmdHostConfig]:
        """コマンド収集ホスト設定情報プロパティ

        インスタンス属性のコマンド収集ホスト設定情報を取得する

        Returns:
            Dict[str, CmdHostConfig]: インスタンス属性のコマンド収集ホスト設定情報
        """
        return self.__cmdHostConfigs

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


class MoConfig:
    """収集設定情報

    OSS連携ホスト名、収集や算出のための設定を保持する

    """

    def __init__(self, mo_host: str, mo_group: str,
                 unitConfigs: Dict[str, UnitConfig]):
        """初期化

        Args:
            mo_host (str): OSS連携ホスト名 OSSから参照されるホスト名
            mo_group (str): グループ名 ホストが属するグループ
            unitConfigs (Dict[str, UnitConfig]): 算出単位設定情報 キーはUnitConfigのunit

        Raises:
            ValueError: output_patternがA、B以外の場合に発生
        """
        self.__mo_host: str = mo_host
        self.__mo_group: str = mo_group
        self.__unitConfigs: Dict[str, UnitConfig] = unitConfigs

    @property
    def mo_host(self) -> str:
        """OSS連携ホスト名プロパティ

        インスタンス属性のOSS連携ホスト名を取得する

        Returns:
            str: インスタンス属性のOSS連携ホスト名
        """
        return self.__mo_host

    @property
    def mo_group(self) -> str:
        """グループ名プロパティ

        インスタンス属性のグループ名を取得する

        Returns:
            str: インスタンス属性のグループ名
        """
        return self.__mo_group

    @property
    def unitConfigs(self) -> Dict[str, UnitConfig]:
        """算出単位設定情報プロパティ

        インスタンス属性の算出単位設定情報を取得する

        Returns:
            Dict[str, UnitConfig]: インスタンス属性の算出単位設定情報
        """
        return self.__unitConfigs

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

    ホスト設定情報ファイルを読み込み、ファイルに設定された収集設定情報、接続設定情報、収集設定情報をコマンド収集ホスト毎に集約したコマンド収集ホスト設定情報を保持する

    """

    def __init__(self, config_file_name: str):
        """初期化

        引数で指定されたホスト設定情報ファイルを読み込み、インスタンス属性に保持する

        Args:
            config_file_name (str): ホスト設定情報ファイルパス
        """
        config_file = pd.ExcelFile(config_file_name, engine='openpyxl')
        self.__moConfigs: Dict[str, MoConfig] = Config.__load_collect_info(config_file)
        self.__cmdHostConfigs: Dict[str, CmdHostConfig] = Config.__load_nf_host_info(self.__moConfigs)
        self.__connectConfigs: List[ConnectConfig] = Config.__load_connect_info(config_file)

    @property
    def moConfigs(self) -> Dict[str, MoConfig]:
        """収集設定情報プロパティ

        インスタンス属性の収集設定情報を取得する

        Returns:
            Dict[str, MoConfig]: 収集設定情報
        """
        return self.__moConfigs

    @property
    def connectConfigs(self) -> List[ConnectConfig]:
        """接続設定情報プロパティ

        インスタンス属性の接続設定情報を取得する

        Returns:
            List[ConnectConfig]: 接続設定情報
        """
        return self.__connectConfigs

    @property
    def cmdHostConfigs(self) -> List[CmdHostConfig]:
        """コマンド収集ホスト設定情報プロパティ

        インスタンス属性のコマンド収集ホスト設定情報（収集設定情報からコマンド収集ホスト単位に集約した情報）を取得する

        Returns:
            Dict[str, CmdHostConfig]: コマンド収集ホスト設定情報
        """
        return self.__cmdHostConfigs

    def __load_collect_info(config_file: pd.ExcelFile) -> Dict[str, MoConfig]:
        """収集設定情報ロード

        設定情報ファイルの「収集情報」シートから情報を読み込み、収集設定情報として返却する

        Args:
            config_file (pd.ExcelFile): ホスト設定情報ファイル（pandasでExcelファイルを表すクラスのオブジェクト）

        Returns:
            Dict[str, MoConfig]: 収集設定情報 キーはOSS連携ホスト
        """
        # 設定情報ファイルから「収集情報」シートの情報を読み込む
        collect_sheet = config_file.parse('収集情報')
        # 収集設定情報辞書を初期化する
        moConfigs: Dict[str, MoConfig] = {}
        # 収集単位設定情報辞書を初期化する
        unitConfigs: Dict[str, UnitConfig] = {}
        # コマンド収集ホスト設定情報辞書を初期化する
        cmdHostConfigs: Dict[str, CmdHostConfig] = {}
        # コマンド設定情報辞書を初期化する
        cmdConfigs: Dict[str, CmdConfig] = {}
        # カウンタ設定情報辞書を初期化する
        counterConfigs: Dict[str, CounterConfig] = {}
        # 収集情報シートの行でループする
        for row in [AsciiFilter(row) for _, row in collect_sheet.iterrows()]:
            # 収集情報シートの行のOSS連携ホスト名がnullでない場合
            if not pd.isnull(row.mo_host):
                # 収集単位設定情報辞書を初期化する
                unitConfigs: Dict[str, UnitConfig] = {}
                # 収集設定情報を収集情報シートの行の情報と収集単位設定情報辞書で生成し、収集設定情報辞書にOSS連携ホスト名をキーとして追加する
                moConfigs[row.mo_host] = MoConfig(row.mo_host, row.mo_group, unitConfigs)
            # 収集情報シートの行の固定値返却フラグがnullでない場合
            if not pd.isnull(row.fixed_response_flag):
                # コマンド収集ホスト設定情報辞書を初期化する
                cmdHostConfigs: Dict[str, CmdHostConfig] = {}
                # 収集情報シートの行の固定値返却フラグがTrueの場合
                if (bool(row.fixed_response_flag)):
                    # 集計単位設定情報を収集情報シートの行の固定値返却フラグと返却固定値（他の値は空または0）で生成し、収集単位設定情報辞書に単位をキーとして追加する
                    unitConfigs[row.unit] = UnitConfig(True, row.fixed_response_message, row.unit, '', 0, 0, 0, 0, cmdHostConfigs)
                # 収集情報シートの行の固定値返却フラグがFalseの場合
                else:
                    # 集計単位設定情報を収集情報シートの行の情報とコマンド収集ホスト設定情報辞書で生成し、収集単位設定情報辞書に単位をキーとして追加する
                    unitConfigs[row.unit] = UnitConfig(False, row.fixed_response_message, row.unit, row.output_pattern,
                                                       int(row.start_duration), int(row.end_duration), int(row.record_num),
                                                       int(row.required_record_percent), cmdHostConfigs)
            # 収集情報シートの行のコマンド収集ホスト名がnullでない場合
            if not pd.isnull(row.nf_host):
                # コマンド設定情報辞書を初期化する
                cmdConfigs: Dict[str, CmdConfig] = {}
                # コマンド収集ホスト設定情報を収集情報シートの行の情報とコマンド設定情報辞書で生成し、コマンド収集ホスト設定情報辞書にコマンド収集ホスト名をキーとして追加する
                cmdHostConfigs[row.nf_host] = CmdHostConfig(row.nf_host, cmdConfigs)
            # 収集情報シートの行のコマンド名がnullでない場合
            if not pd.isnull(row.cmd):
                # カウンタ設定情報辞書を初期化する
                counterConfigs: Dict[str, CounterConfig] = {}
                # コマンド設定情報を収集情報シートの行の情報とカウンタ設定情報辞書で生成し、コマンド設定情報辞書にコマンド名をキーとして追加する
                cmdConfigs[row.cmd] = CmdConfig(row.cmd, counterConfigs)
            # 収集情報シートの行の結果カウンタ名がnullでない場合
            if not pd.isnull(row.counter_name):
                # カウンタ設定情報を収集情報シートの行の情報で生成し、カウンタ設定情報辞書に結果カウンタ名をキーとして追加する
                counterConfigs[row.counter_name] = CounterConfig(row.cmd_count_item, row.counter_name, row.aggregate_type)
        # 収集設定情報辞書を返却する
        return moConfigs

    def __load_nf_host_info(moConfigs: Dict[str, MoConfig]) -> Dict[str, CmdHostConfig]:
        """コマンド収集ホスト設定情報ロード

        収集設定情報からコマンド収集ホスト単位に情報を集約し、コマンド収集ホスト設定情報として返却する

        Args:
            moConfigs (Dict[str, MoConfig]): 収集設定情報

        Returns:
            Dict[str, CmdHostConfig]: コマンド収集ホスト設定情報
        """
        # コマンド収集ホスト設定情報辞書を初期化する
        cmdHostDict: Dict[str, CmdHostConfig] = {}
        # 引数の収集設定情報の項目でループする
        for moConfigTpl in moConfigs.items():
            # 収集設定情報の収集単位設定情報の項目でループする
            for unitConfigTpl in moConfigTpl[1].unitConfigs.items():
                # 収集単位設定情報のコマンド収集ホスト設定情報の項目でループする
                for cmdHostConfigTpl in unitConfigTpl[1].cmdHostConfigs.items():
                    # コマンド収集ホスト設定情報のコマンド収集ホスト名がコマンド収集ホスト設定情報辞書に登録されていない場合
                    if cmdHostConfigTpl[0] not in cmdHostDict:
                        # コマンド収集ホスト設定情報の情報から登録用コマンド収集ホスト設定情報を生成し、コマンド収集ホスト設定情報辞書に登録する（コマンド設定情報は空で生成する）
                        cmdHostDict[cmdHostConfigTpl[0]] = CmdHostConfig(cmdHostConfigTpl[0], {})
                    # コマンド収集ホスト設定情報辞書に登録されているコマンド収集ホスト設定情報を登録コマンド収集ホスト設定情報として取得する
                    cmdHost = cmdHostDict.get(cmdHostConfigTpl[0])
                    # コマンド収集ホスト設定情報のコマンド設定情報の項目でループする
                    for cmdConfigTpl in cmdHostConfigTpl[1].cmdConfigs.items():
                        # コマンド設定情報のコマンド名が登録コマンド収集ホスト設定情報のコマンド設定情報に登録されていない場合
                        if cmdConfigTpl[0] not in cmdHost.cmdConfigs:
                            # コマンド設定情報を生成し、登録コマンド収集ホスト設定情報のコマンド設定情報に登録する（カウンタ設定情報は空で生成する）
                            cmdHost.cmdConfigs[cmdConfigTpl[0]] = CmdConfig(cmdConfigTpl[0], {})
                        # 登録コマンド収集ホスト設定情報のコマンド設定情報に登録されているコマンド設定情報を登録コマンド設定情報として取得する
                        cmd = cmdHost.cmdConfigs.get(cmdConfigTpl[0])
                        # 引数の収集設定情報.収集単位設定情報.コマンド収集ホスト設定情報.コマンド設定情報のカウンタ設定情報の項目でループする
                        for counterConfigTpl in cmdConfigTpl[1].counterConfigs.items():
                            # 引数の収集設定情報.収集単位設定情報.コマンド収集ホスト設定情報.コマンド設定情報.カウンタ設定情報の結果カウンタ名が登録コマンド設定情報のカウンタ設定情報に登録されていない場合
                            if cmdConfigTpl[0] not in cmd.counterConfigs:
                                # カウンタ設定情報を生成し、登録コマンド設定情報のカウンタ設定情報に登録する
                                cmd.counterConfigs[counterConfigTpl[0]] = CounterConfig(
                                    counterConfigTpl[1].cmd_count_item, counterConfigTpl[1].counter_name, None)
        # コマンド収集ホスト設定情報辞書を返却する
        return cmdHostDict

    def __load_connect_info(config_file: pd.ExcelFile) -> List[ConnectConfig]:
        """接続設定情報ロード

        設定情報ファイルの「接続情報」シートから情報を読み込み、接続設定情報として返却する
        収集ホスト設定情報配下の接続設定情報はpriority、bastionの昇順でソートされる

        Args:
            config_file (pd.ExcelFile): ホスト設定情報ファイル（pandasでExcelファイルを表すオブジェクト）

        Returns:
            List[ConnectConfig]: 接続設定情報
        """
        # 設定情報ファイルから「接続情報」シートの情報を読み込む
        connect_sheet = config_file.parse('接続情報')
        # 接続設定情報リストを初期化する
        connectConfigs: List[ConnectConfig] = []
        # 接続情報シートの行でループする
        for row in [AsciiFilter(row) for _, row in connect_sheet.iterrows()]:
            # 接続情報シートの行のコマンド収集ホスト名がnullでない場合
            if not pd.isnull(row.nf_host):
                # 接続ホスト設定情報リストを初期化する
                accessHostConfigs: List[AccessHostConfig] = []
                # 接続情報シートの行の情報と接続ホスト設定情報リストから接続設定情報を生成し、接続設定情報リストに追加する
                connectConfigs.append(
                    ConnectConfig(row.nf_host, row.vendor, row.nf_type, bool(row.enable_flag), bool(row.close_flag),
                                  accessHostConfigs))
            # 接続情報シートの行の接続ホスト名がnullでない場合
            if not pd.isnull(row.access_host):
                # 接続情報シートの行の情報で接続ホスト設定情報を生成し、接続ホスト設定情報に追加する
                accessHostConfigs.append(
                    AccessHostConfig(row.access_host, row.nf_ip, int(row.nf_auth_method), row.nf_user, row.nf_password, row.nf_key_info,
                                     int(row.priority), int(row.bastion)))
        # 接続設定情報リストでループする
        for connectConfig in connectConfigs:
            # 接続設定情報の接続ホスト設定情報が２つ以上存在する場合
            if len(connectConfig.accessHostConfigs) >= 2:
                # 接続設定情報の接続ホスト設定情報を優先順位、多段接続の昇順でソートする
                bastion_digits: int = len(str(max([accessHostConfig.bastion for accessHostConfig in connectConfig.accessHostConfigs])))
                connectConfig.accessHostConfigs.sort(key=lambda x: x.priority*(10**bastion_digits) + x.bastion)
            else:
                pass
        return connectConfigs

    def get_MoConfig_by_mo_host(self, mo_host: str) -> MoConfig:
        """収集設定情報取得

        指定されたOSS連携ホスト名に関連する収集設定情報を、保持している収集設定情報から取得する

        Args:
            mo_host (str): OSS連携ホスト名

        Returns:
            MoConfig: 指定されたOSS連携ホスト名に関連する収集設定情報
        """
        return self.__moConfigs.get(mo_host)

    def get_ConnectConfig_by_nf_host(self, nf_host: str) -> ConnectConfig:
        """接続設定情報取得

        指定されたコマンド収集ホスト名に関連する接続設定情報を、保持している接続設定情報から取得する

        Args:
            nf_host (str): コマンド収集ホスト名

        Returns:
            ConnectConfig: 指定されたコマンド収集ホスト名に関連する接続設定情報
        """
        for connectConfig in self.__connectConfigs:
            if connectConfig.nf_host == nf_host:
                return connectConfig
        return None

    def get_cmdHostConfig_by_nf_host(self, nf_host: str) -> CmdHostConfig:
        """コマンド収集ホスト設定情報取得

        指定されたコマンド収集ホスト名に関連するコマンド収集ホスト設定情報を保持しているコマンド収集ホスト設定情報から取得する

        Args:
            nf_host (str): コマンド収集ホスト名

        Returns:
            CmdHostConfig: コマンド収集ホスト設定情報
        """
        return self.__cmdHostConfigs.get(nf_host)


if __name__ == '__main__':
    config_file_name = 'C:\\FY23_GCP2.0\\T1AR001\\bin\\impact_sampling_config.xlsx'
    config = Config(config_file_name)
    # print(config.moConfigs.values())
    # for mohost in config.moConfigs.values():
    #     print(mohost.mo_host)
    #     # print(type(mohost.mo_host))
    #     tam_host = mohost.mo_host.replace("001", "")
    #     print(tam_host)
    #     print(mohost.mo_host)
    # print(config.cmdHostConfigs['tam5-er-s01-amf-001'])
    # print(config.cmdHostConfigs['tam5-er-s01-amf-001']._CmdHostConfig__cmdConfigs.keys())
    # print(config.connectConfigs[0])
    # print(type(config.moConfigs))
    print(config.get_cmdHostConfig_by_nf_host('tam5-er-s01-amf-001'))