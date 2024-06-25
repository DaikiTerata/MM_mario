"""ホスト設定情報

ホスト設定情報エクセルファイルを読み込み、読み込んだ情報を提供する

"""
import re
import pandas as pd
import pandas.core.series
import openpyxl
from typing import List, Dict, Any

from MM_ListConfig import ListConfig
from ListRow import ListRow


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

class ListLoadConfig:
    """接続設定情報

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
        # リストシート名リスト初期化
        list_sheet_list: List = []
        # 設定ファイルのシート名リストから、各シート名を繰り返し取り出す
        for sheet_name in config_sheet_name:
            # シート名に「LIST001」がある場合
            if 'LIST' in sheet_name:
                # 接続設定情報シート名設定
                list_sheet_list.append(sheet_name)
        # 読み込んだ設定ファイルと接続設定情報シート名を引数に、接続設定情報ロードを呼び出す
        self.__listConfigs: Dict[str, ListConfig] = ListLoadConfig.__load_list_info(config_file, list_sheet_list)

    @property
    def listConfigs(self) -> Dict[str, ListConfig]:
        """接続設定情報プロパティ

        インスタンス属性の接続設定情報を取得する
        接続設定情報シートがある限り、読み込む

        Returns:
            Dict[str, ListConfig]: 接続設定情報
        """
        return self.__listConfigs

    def __load_list_info(config_file: pd.ExcelFile, list_sheet_list: List) -> Dict[str, ListConfig]:
        """接続設定情報ロード

        シナリオ設定情報ファイルの「LIST」シートから情報を読み込み、接続設定情報として返却する
        「LIST」シートがある限り、設定情報を読み込む

        Args:
            config_file (pd.ExcelFile): シナリオ設定情報ファイル（pandasでExcelファイルを表すオブジェクト）

        Returns:
            Dict[str, ListConfig]: 接続設定情報
        """
        # 接続設定情報を初期化する
        listConfigs: List[ListConfig] = []
        # 引渡されたリストシート名リストに格納されているリストシート名を順に呼び出す
        for list_sheet_name in list_sheet_list:
            # リストに格納されている順に取得したリスト名のシナリオ取得
            list_collect_sheet = config_file.parse(list_sheet_name)
            # LISTシートの行でループする
            for row in [AsciiFilter(row) for _, row in list_collect_sheet.iterrows()]:
                # 各列の1行目をキー、2行目以降を値として格納しているものを変数化
                list_row_items = row.__dict__.items()
                # 各行情報リストを初期化
                list_row_vallist = []
                for list_row_key, list_row_val in list_row_items:
                    # 各行の情報を格納
                    list_row_vallist.append(list_row_val)
                # LISTシートの行のコマンド実行ホスト名"HOST"がnullでない場合
                if not pd.isnull(row.cNRF_AMF):
                    # LISTシートの行の情報から接続設定情報を生成し、接続設定情報リストに追加する
                    listConfigs.append(ListConfig(*list_row_vallist))
        return listConfigs

    # def get_scenario(self, scenario: str) -> ScenarioConfig:
    #     """シナリオ設定情報取得

    #     指定されたシナリオ名に関連する設定情報を、保持しているシナリオ設定情報から取得する

    #     Args:
    #         scenario(str): シナリオ名

    #     Returns:
    #         ScenarioConfig: 指定されたシナリオ名に関連するシナリオ設定情報
    #     """
    #     return self.__subConfigs.get(scenario)

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
    config = ListLoadConfig(config_file_name)
    # print(len(config.listConfigs))
    cNRF_AMF_list = ListConfig.get__cNRF_AMF_list()
    print(len(cNRF_AMF_list))
    for i in cNRF_AMF_list:
        print(i)
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

    # for i in config.listConfigs:
    #     print(i)

    # # print(config.subConfigs[0]._ScenarioConfig__commandConfigs[0])
    # print(config.listConfigs)
    # print()
    # print()

    # print(config.mainConfigs)
    # print(config.mainConfigs["timeout"]._MainConfig__value)
    # print(type(config.mainConfigs["timeout"]._MainConfig__value))

    # for key, val in config.mainConfigs.items():
    #     # print(key, val)
    #     print(key)
    #     print(val._MainConfig__value)
    #     print()
    #     print()

    # for key, val in config.subConfigs.items():
    #     # print(key, val)
    #     print(key)
    #     # print(val)
    #     # print(val._ScenarioConfig__commandConfigs)
    #     print()
    #     # print()
    #     for dp_key, dp_val  in val._ScenarioConfig__commandConfigs.items():
    #         # print(dp_key, dp_val)
    #         print(dp_key)
    #         print(dp_val)
    #         print()
    #         print()

    # for key, val in config.listConfigs.items():
    #     # print(key, val)
    #     print(key)
    #     print(val)
    #     # print(val._ScenarioConfig__commandConfigs)
    #     print()
    #     print()
    #     # for dp_key, dp_val  in val.items():
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
    