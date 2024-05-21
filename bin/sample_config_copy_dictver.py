"""ホスト設定情報

ホスト設定情報エクセルファイルを読み込み、読み込んだ情報を提供する

"""
import re
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


class CommandConfig:
    """実行コマンド設定情報

    実行するコマンドの設定を保持する

    """

    def __init__(self, node: str, item: str, command: str, when: str, check_kind: str, result_OK: str, result_NG: str, option: str):
        """初期化

        Args:
            node (str): 実行環境名 コマンド実行する環境
            item (str): コマンド概要項目 実行するコマンドの概要
            command (str): コマンド名 実行するコマンド
            when (str): 実行条件項目 コマンドを実行する条件の項目            
            check_kind (str): 確認条件項目 result_OK/result_NGで確認する条件
            result_OK (str): 正常結果判定項目 コマンド実行結果と比較して正常と判定される項目名
            result_NG (str): 異常結果判定項目 コマンド実行結果と比較して異常と判定される項目名
            option (str): 後続処理判定項目 エラー時、後続処理を停止するか判定する項目 disableである場合は後続処理を停止せずに実行、ableの場合は後続処理を停止させる
        """
        self.__node: str = node
        self.__item: str = item
        self.__command: str = command
        self.__when: str = when
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
    def item(self) -> str:
        """コマンド概要項目情報プロパティ

        インスタンス属性のコマンド概要項目を取得する

        Returns:
            str: インスタンス属性のコマンド概要項目
        """
        return self.__item

    @property
    def command(self) -> str:
        """コマンドプロパティ

        インスタンス属性のコマンドを取得する

        Returns:
            str: インスタンス属性のコマンド
        """
        return self.__command
    
    @property
    def when(self) -> str:
        """実行条件項目プロパティ

        インスタンス属性の実行条件項目を取得する

        Returns:
            str: インスタンス属性の実行条件項目
        """
        return self.__when

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
    def commandConfigs(self) -> Dict[str, CommandConfig]:
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

    @property
    def subConfigs(self) -> Dict[str, ScenarioConfig]:
        """サブ001設定情報プロパティ

        インスタンス属性のサブ001設定情報を取得する

        Returns:
            Dict[str, ScenarioConfig]: サブ001設定情報
        """
        return self.__subConfigs

    def __load_main_process_info(config_file: pd.ExcelFile) -> Dict[str, ScenarioConfig]:
        """メイン設定情報ロード

        シナリオ設定情報ファイルの「MAIN」シートから情報を読み込み、メイン設定情報として返却する

        Args:
            config_file (pd.ExcelFile): ホスト設定情報ファイル（pandasでExcelファイルを表すクラスのオブジェクト）

        Returns:
            maiConfigs: Dict[str, ScenarioConfig]: メイン設定情報 キーはシナリオ名
        """
        # 「MAIN」シート名設定
        config_sheet_name = 'MAIN'
        # 設定情報ファイルから「MAIN」シートの情報を読み込む
        main_collect_sheet = config_file.parse(config_sheet_name)
        # シナリオ設定情報辞書を初期化する
        mainConfigs: Dict[str, ScenarioConfig] = {}
        # コマンド設定情報辞書を初期化する
        commandConfigs: Dict[str, CommandConfig] = {}

        # MAINシートの行でループする
        for row in [AsciiFilter(row) for _, row in main_collect_sheet.iterrows()]:
            # MAINシートの行のシナリオ名がnullでない場合
            if not pd.isnull(row.SCENARIO):
                # 実行環境設定情報辞書を初期化する
                commandConfigs: Dict[str, CommandConfig] = {}
                # シナリオ設定情報をMAINシートの行の情報と実行コマンド設定情報辞書で生成し、シナリオ設定情報辞書にシナリオ名"SCENARIO"をキーとして追加する
                mainConfigs[row.SCENARIO] = ScenarioConfig(row.SCENARIO, commandConfigs)
            
            if 'loop_dns' in row.ITEM:
                ###### loop_dns_show/del/addの結果を参照する処理を追加？
                
                ###### SHOW/DOWN/UPのいずれかを検知したらTrueに、それ以外はFalse
                mode_check_result = True
                if mode_check_result:
                    # 検知した文字列の抽出
                    pattern = re.compile(r'[A-Z]{3}[0-9]{3}')
                    sub_sheet_name: str = pattern.search(row.COMMAND).group(0)
                    sub_collect_sheet = config_file.parse(sub_sheet_name)
                    sub_config = Config.__load_sub_process_info(sub_collect_sheet, sub_sheet_name)
                    sub_flg = True

            # MAINシートの行の実行環境名がnullでない場合
            if not pd.isnull(row.NODE):
                # 実行コマンド設定情報をMAINシートの行の情報で生成し、実行コマンド設定情報辞書に実行コマンド項目名"ITEM"をキーとして追加する
                commandConfigs[f'{config_sheet_name}_{row.ITEM}'] = CommandConfig(row.NODE, row.ITEM, row.COMMAND, row.WHEN, 
                                                                                  row.CHECK_KIND, row.RESULT_OK, row.RESULT_NG, row.OPTION)
                if 'SUB' in row.COMMAND and sub_flg :
                    commandConfigs[sub_sheet_name] = sub_config

        # 収集設定情報辞書を返却する
        return mainConfigs


    def __load_sub_process_info(sub_collect_sheet: pd.DataFrame, sub_sheet_name: str) -> Dict[str, ScenarioConfig]:
        """サブ設定情報ロード

        シナリオ設定情報ファイルの「SUB」シートから情報を読み込み、サブ設定情報として返却する

        Args:
            config_file (pd.ExcelFile): ホスト設定情報ファイル（pandasでExcelファイルを表すクラスのオブジェクト）

        Returns:
            subConfigs: Dict[str, ScenarioConfig]: サブ設定情報 キーはシナリオ名
        """
        # if sub_sheet_name == 'SUB001':
            # シナリオ設定情報辞書を初期化する
        subConfigs: Dict[str, ScenarioConfig] = {}
        # コマンド設定情報辞書を初期化する
        commandConfigs: Dict[str, CommandConfig] = {}

        # SUBシートの行でループする
        for row in [AsciiFilter(row) for _, row in sub_collect_sheet.iterrows()]:
            # SUBシートの行のシナリオ名がnullでない場合
            if not pd.isnull(row.SCENARIO):
                # 実行環境設定情報辞書を初期化する
                commandConfigs: Dict[str, CommandConfig] = {}
                # シナリオ設定情報をSUB001シートの行の情報と実行コマンド設定情報辞書で生成し、シナリオ設定情報辞書にシナリオ名"SCENARIO"をキーとして追加する
                subConfigs[row.SCENARIO] = ScenarioConfig(row.SCENARIO, commandConfigs)

            # SUBシートの行の実行環境名がnullでない場合
            if not pd.isnull(row.NODE):
                # 実行コマンド設定情報をSUBシートの行の情報で生成し、実行コマンド設定情報辞書に実行コマンド項目名"ITEM"をキーとして追加する
                commandConfigs[f'{sub_sheet_name}_{row.ITEM}'] = CommandConfig(row.NODE, row.ITEM, row.COMMAND, row.WHEN, 
                                                                                row.CHECK_KIND, row.RESULT_OK, row.RESULT_NG, row.OPTION)
        # 収集設定情報辞書を返却する
        return subConfigs

        # else:
        #     pass


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
    # print(config._Config__mainConfigs['main']._ScenarioConfig__commandConfigs)
    # dict = config._Config__mainConfigs
    for key, val in config._Config__mainConfigs['main']._ScenarioConfig__commandConfigs.items():
        # print(val._CommandConfig__item)
        # print(val)
        if key == 'SUB001':
            print(val)
        else:
            continue
    # print(type(dict))
    print()
    print()
    # print(config._Config__sub001Configs)