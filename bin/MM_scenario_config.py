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

    def __init__(self, node: str, no: str, task: str, item: str, when: str, command: str, var: str,
                check_kind: str, result_OK: str, result_NG: str, option: str):
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
        # 設定ファイル読み込み
        config_file = pd.ExcelFile(config_file_name, engine='openpyxl')
        # 設定ファイルのシート名読み込み（返却値はList型）
        config_sheet_name: List = config_file.sheet_names
        # サブシート名リスト初期化
        sub_sheet_list: List = []
        # リストシート名リスト初期化
        list_sheet_list: List = []
        # 設定ファイルのシート名リストから、各シート名を繰り返し取り出す
        for sheet_name in config_sheet_name:
            # シート名が「MAIN」である場合
            if 'MAIN' in sheet_name:
                # メインシート名設定
                main_sheet_name: str = sheet_name
            # シート名に「SUB」が含まれる場合
            elif 'SUB' in sheet_name:
                # サブシート名リストに格納
                sub_sheet_list.append(sheet_name)
            # シート名に「LIST001」がある場合
            elif 'LIST' in sheet_name:
                # 接続設定情報シート名設定
                list_sheet_list.append(sheet_name)
        # 読み込んだ設定ファイルとメインシート名を引数に、メイン設定情報ロードを呼び出す
        self.__mainConfigs: Dict[str, MainConfig] = Config.__load_main_info(config_file, main_sheet_name)
        # 読み込んだ設定ファイルとサブシート名リストを引数に、サブ設定情報ロードを呼び出す
        self.__subConfigs: Dict[str, ScenarioConfig] = Config.__load_sub_process_info(config_file, sub_sheet_list)
        # 読み込んだ設定ファイルと接続設定情報シート名を引数に、接続設定情報ロードを呼び出す
        self.__listConfigs: List[ListConfig] = Config.__load_list_info(config_file, list_sheet_list)

    @property
    def mainConfigs(self) -> Dict[str, MainConfig]:
        """初期設定情報プロパティ

        インスタンス属性の初期設定情報を取得する

        Returns:
            Dict[str, MainConfig]: 初期設定情報
        """
        return self.__mainConfigs

    @property
    def subConfigs(self) -> Dict[str, ScenarioConfig]:
        """サブ設定情報プロパティ

        インスタンス属性のサブ設定情報を取得する
        サブ設定情報シートがある限り、読み込む

        Returns:
            Dict[str, ScenarioConfig]: サブ設定情報
        """
        return self.__subConfigs

    @property
    def listConfigs(self) -> List[ListConfig]:
        """接続設定情報プロパティ

        インスタンス属性の接続設定情報を取得する
        接続設定情報シートがある限り、読み込む

        Returns:
            List[ListConfig]: 接続設定情報
        """
        return self.__listConfigs

    def __load_main_info(config_file: pd.ExcelFile, main_sheet_name: str) -> Dict[str, MainConfig]:
        """メイン設定情報ロード

        シナリオ設定情報ファイルの「MAIN」シートから情報を読み込み、メイン設定情報として返却する

        Args:
            config_file (pd.ExcelFile): シナリオ設定情報ファイル（pandasでExcelファイルを表すオブジェクト）

        Returns:
            Dict[str, MainConfig]: 初期設定情報
        """
        # シナリオ設定情報ファイルから「DEFAULT_OPTION」シートの情報を読み込む
        main_sheet = config_file.parse(main_sheet_name)
        # 接続設定情報リストを初期化する
        mainConfigs: Dict[str, MainConfig] = {}
        # DEFAULT_OPTIONシートの行でループする
        for row in [AsciiFilter(row) for _, row in main_sheet.iterrows()]:
            # DEFAULT_OPTIONシートの行の初期設定項目名"KEY"がnullでない場合
            if not pd.isnull(row.KEY):
                # DEFAULT_OPTIONシートの行の情報から初期設定情報辞書を生成し、初期設定項目名"KEY"をキーに初期設定情報辞書に追加する
                mainConfigs[row.KEY] = MainConfig(row.KEY, row.VALUE)

        return mainConfigs


    def __load_sub_process_info(config_file: pd.DataFrame, sub_sheet_list: Dict) -> Dict[str, ScenarioConfig]:
        """サブ設定情報ロード

        シナリオ設定情報ファイルの「SUB」シートから情報を読み込み、サブ設定情報として返却する
        「SUB」シートがある限り、設定情報を読み込む

        Args:
            config_file (pd.ExcelFile): ホスト設定情報ファイル（pandasでExcelファイルを表すクラスのオブジェクト）

        Returns:
            subConfigs: Dict[str, ScenarioConfig]: サブ設定情報 キーはシナリオ名
        """
        # シナリオ設定情報辞書を初期化する
        subConfigs: Dict[str, ScenarioConfig] = {}
        # コマンド設定情報辞書を初期化する
        commandConfigs: Dict[str, CommandConfig] = {}
        # 引渡されたサブシート名リストに格納されているサブシート名を順に呼び出す
        for sub_sheet_name in sub_sheet_list:
            # リストに格納されている順に取得したサブシート名のシナリオ設定ファイルを取得
            sub_collect_sheet = config_file.parse(sub_sheet_name)
            # SUBシートの行でループする
            for row in [AsciiFilter(row) for _, row in sub_collect_sheet.iterrows()]:
                # SUBシートの行のシナリオ名がnullでない場合
                if not pd.isnull(row.SCENARIO):
                    # コマンド設定情報辞書を初期化する
                    commandConfigs: Dict[str, CommandConfig] = {}
                    # シナリオ設定情報をSUB001シートの行の情報と実行コマンド設定情報辞書で生成し、シナリオ設定情報辞書にシナリオ名"SCENARIO"をキーとして追加する
                    subConfigs[row.SCENARIO] = ScenarioConfig(row.SCENARIO, commandConfigs)

                # SUBシートの行の実行環境名がnullでない場合
                if not pd.isnull(row.NODE):
                    # 実行コマンド設定情報をSUBシートの行の情報で生成し、実行コマンド設定情報辞書に実行コマンド項目名"ITEM"をキーとして追加する
                    commandConfigs[row.SCENARIO] = CommandConfig(row.NODE, row.NO, row.TASK, row.ITEM, row.WHEN, row.COMMAND, 
                                                        row.VAR, row.CHECK_KIND, row.RESULT_OK, row.RESULT_NG, row.OPTION)
        # 収集設定情報辞書を返却する
        return subConfigs


    def __load_list_info(config_file: pd.ExcelFile, list_sheet_list: List) -> List[ListConfig]:
        """接続設定情報ロード

        シナリオ設定情報ファイルの「LIST」シートから情報を読み込み、接続設定情報として返却する
        「LIST」シートがある限り、設定情報を読み込む

        Args:
            config_file (pd.ExcelFile): シナリオ設定情報ファイル（pandasでExcelファイルを表すオブジェクト）

        Returns:
            List[ListConfig]: 接続設定情報
        """
        # 接続設定情報リストを初期化する
        listConfigs: List[ListConfig] = []
        # 引渡されたリストシート名リストに格納されているリストシート名を順に呼び出す
        for list_sheet_name in list_sheet_list:
            # リストに格納されている順に取得したリスト名のシナリオ取得
            list_collect_sheet = config_file.parse(list_sheet_name)
            # LISTシートの行でループする
            for row in [AsciiFilter(row) for _, row in list_collect_sheet.iterrows()]:
                # LISTシートの行のコマンド実行ホスト名"HOST"がnullでない場合
                if not pd.isnull(row.HOST):
                    # LISTシートの行の情報から接続設定情報を生成し、接続設定情報リストに追加する
                    listConfigs.append(ListConfig(row.NF, row.REMOTE_HOST, row.cNRF_AMF, row.cNRF, row.HOST,
                                                         row.DN, row.NS, row.IP, row.VER,row.REGION, row.DEL_FLG))
        return listConfigs

    def get_scenario(self, scenario: str) -> ScenarioConfig:
        """シナリオ設定情報取得

        指定されたシナリオ名に関連する設定情報を、保持しているシナリオ設定情報から取得する

        Args:
            scenario(str): シナリオ名

        Returns:
            ScenarioConfig: 指定されたシナリオ名に関連するシナリオ設定情報
        """
        return self.__subConfigs.get(scenario)

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
    # print(config.mainConfigs)
    # print()
    # print()

    # print(config.subConfigs)
    # print()
    # print()
    # print(config.get_scenario('amf_dns_up'))

    # print(config.listConfigs)
    # print()
    # print()

    # # print(config.subConfigs[0]._ScenarioConfig__commandConfigs[0])
    # print(config.listConfigs)
    # print()
    # print()

    # print(config.mainConfigs)
    # print(config.mainConfigs["timeout"]._MainConfig__value)
    # print(type(config.mainConfigs["timeout"]._MainConfig__value))

    # for val in config.mainConfigs:
    #     print(val)
    #     print()
    #     print()

    for key, val in config.subConfigs.items():
        # print(key, val)
        # print(key)
        # print(val)
        # print(val._ScenarioConfig__commandConfigs)
        print()
        print()
        for dp_key, dp_val  in val._ScenarioConfig__commandConfigs.items():
            print(dp_key, dp_val)

    # for val in config.listConfigs:
    #     print(val)
    #     print()
    #     print()

    # for key, val in config.mainConfigs.items():
    #     print(key,val)
    #     print(key)
    #     print(val._MainConfig__value)
    #     print(type(val._MainConfig__value))
    #     print()
    #     print()

    # print()
    # print()
    