"""ホスト設定情報

ホスト設定情報エクセルファイルを読み込み、読み込んだ情報を提供する

"""
import re
import pandas as pd
import pandas.core.series
import openpyxl
from typing import List, Dict, Any

from MM_CommandConfig import CommandConfig
from MM_ScenarioConfig import ScenarioConfig
from MM_ListConfig import ListConfig
from MM_MainConfig import MainConfig


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
        self.__listConfigs: Dict[str, ListConfig] = Config.__load_list_info(config_file, list_sheet_list)

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
    def listConfigs(self) -> Dict[str, ListConfig]:
        """接続設定情報プロパティ

        インスタンス属性の接続設定情報を取得する
        接続設定情報シートがある限り、読み込む

        Returns:
            Dict[str, ListConfig]: 接続設定情報
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
        # 引渡されたサブシート名リストに格納されているサブシート名を順に呼び出す
        for sub_sheet_name in sub_sheet_list:
            # リストに格納されている順に取得したサブシート名のシナリオ設定ファイルを取得
            sub_collect_sheet = config_file.parse(sub_sheet_name)
            # SUBシートの行でループする
            for row in [AsciiFilter(row) for _, row in sub_collect_sheet.iterrows()]:
                rowkeys = row.__dict__.items()
                print(rowkeys)
                # rowlist = []
                # for key, val in rowkeys:
                #     rowlist.append(val)
                # print(rowlist)
                # SUBシートの行のシナリオ名がnullでない場合
                if not pd.isnull(row.NO):
                    # シナリオ設定情報をSUB001シートの行の情報と実行コマンド設定情報辞書で生成し、シナリオ設定情報辞書にシナリオ名"SCENARIO"をキーとして追加する
                    subConfigs[row.SCENARIO] = ScenarioConfig(row.SCENARIO, row.NODE, row.NO, row.TASK, row.ITEM, row.WHEN, row.COMMAND, 
                                                        row.VAR, row.CHECK_KIND, row.RESULT_OK, row.RESULT_NG, row.OPTION)

        # 収集設定情報辞書を返却する
        return subConfigs


    def __load_list_info(config_file: pd.ExcelFile, list_sheet_list: List) -> Dict[str, ListConfig]:
        """接続設定情報ロード

        シナリオ設定情報ファイルの「LIST」シートから情報を読み込み、接続設定情報として返却する
        「LIST」シートがある限り、設定情報を読み込む

        Args:
            config_file (pd.ExcelFile): シナリオ設定情報ファイル（pandasでExcelファイルを表すオブジェクト）

        Returns:
            Dict[str, ListConfig]: 接続設定情報
        """
        # 接続設定情報辞書を初期化する
        listConfigs: Dict[str, ListConfig] = {}
        # 引渡されたリストシート名リストに格納されているリストシート名を順に呼び出す
        for list_sheet_name in list_sheet_list:
            # リストに格納されている順に取得したリスト名のシナリオ取得
            list_collect_sheet = config_file.parse(list_sheet_name)
            # LISTシートの行でループする
            for row in [AsciiFilter(row) for _, row in list_collect_sheet.iterrows()]:
                # LISTシートの行のコマンド実行ホスト名"HOST"がnullでない場合
                if not pd.isnull(row.cNRF_AMF):
                    # LISTシートの行の情報から接続設定情報を生成し、接続設定情報リストに追加する
                    listConfigs[row.cNRF_AMF] = ListConfig(row.NF, row.REMOTE_HOST, row.cNRF_AMF, row.cNRF, row.HOST,
                                                         row.DN, row.NS, row.IP, row.VER,row.REGION, row.DEL_FLG)
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
    config_file_name = 'C:\\python\\MM_scenario_config.xlsx'
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
        print(key, val)
        # print(key)
        # print(val)
        # print(val._ScenarioConfig__commandConfigs)
        print()
        print()
        # for dp_key, dp_val  in val._ScenarioConfig__commandConfigs.items():
        #     print(dp_key, dp_val)

    # for key, val in config.listConfigs.items():
    #     print(key, val)
    #     # print(key)
    #     # print(val)
    #     # print(val._ScenarioConfig__commandConfigs)
    #     print()
    #     print()
    #     # for dp_key, dp_val  in val._ScenarioConfig__commandConfigs.items():
    #     #     print(dp_key, dp_val)

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
    