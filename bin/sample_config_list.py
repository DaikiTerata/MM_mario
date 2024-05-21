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

    def __init__(self, scenario: str, commandConfigs: List[CommandConfig]):
        """初期化

        Args:
            scenario (str): シナリオ名 ツール実行を行うシナリオ名
            commandConfigs (Dict[str, CommandConfig]): 実行コマンド設定情報 キーは実行コマンド概要項目
        """
        self.__scenario: str = scenario
        self.__commandConfigs: List[CommandConfig] = commandConfigs

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
            List[CommandConfig]: インスタンス属性の実行コマンド設定情報
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


class ConnectConfig:
    """接続設定情報

    NF設備への接続のための設定を保持する

    """

    def __init__(self, nf_host: str, nf_dn: str, nf_ds: str, nf_ip: str, nf_ver: int, nf_region: str, nf_del_flg: int) -> None:
        """初期化

        Args:
            nf_host (str): コマンド実行ホスト名 コマンドを実行するホスト名
            nf_dn (str): 
            nf_ds (str): 
            nf_ip (str): 接続先IPアドレス
            nf_ver (int): 
            nf_region(str): 実行地域
            nf_del_flg(int): 

        """
        self.__nf_host: str = nf_host
        self.__nf_dn: str = nf_dn
        self.__nf_ds: str = nf_ds
        self.__nf_ip: str = nf_ip
        self.__nf_ver: int = int(nf_ver)
        self.__nf_region: str = nf_region
        self.__nf_del_flg: int = int(nf_del_flg)


    @property
    def nf_host(self) -> str:
        """コマンド実行ホスト名プロパティ

        インスタンス属性のコマンド実行ホスト名を取得する

        Returns:
            str: インスタンス属性のコマンド実行ホスト名
        """
        return self.__nf_host

    @property
    def nf_dn(self) -> str:
        """プロパティ

        インスタンス属性のを取得する

        Returns:
            str: インスタンス属性の
        """
        return self.__nf_dn

    @property
    def nf_ds(self) -> str:
        """プロパティ

        インスタンス属性のを取得する

        Returns:
            str: インスタンス属性の
        """
        return self.__nf_ds

    @property
    def nf_ip(self) -> bool:
        """接続先IPプロパティ

        インスタンス属性の接続先IPを取得する

        Returns:
            str: インスタンス属性の接続先IP
        """
        return self.__nf_ip

    @property
    def nf_ver(self) -> bool:
        """プロパティ

        インスタンス属性のを取得する

        Returns:
            bool: インスタンス属性の
        """
        return self.__nf_ver

    @property
    def nf_region(self) -> bool:
        """実行地域プロパティ

        インスタンス属性の実行地域を取得する

        Returns:
            bool: インスタンス属性の実行地域
        """
        return self.__nf_region

    @property
    def nf_del_flg(self) -> bool:
        """プロパティ

        インスタンス属性のを取得する

        Returns:
            bool: インスタンス属性の
        """
        return self.__nf_del_flg

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
        self.__mainConfigs: List[ScenarioConfig] = Config.__load_main_process_info(config_file)
        self.__connectConfigs: List[ConnectConfig] = Config.__load_connect_info(config_file)

    @property
    def mainConfigs(self) -> List[ScenarioConfig]:
        """メイン設定情報プロパティ

        インスタンス属性のメイン設定情報を取得する

        Returns:
            List[ScenarioConfig]: メイン設定情報
        """
        return self.__mainConfigs

    @property
    def connectConfigs(self) -> List[ConnectConfig]:
        """接続設定情報プロパティ

        インスタンス属性の接続設定情報を取得する

        Returns:
            List[ConnectConfig]: 接続設定情報
        """
        return self.__connectConfigs

    def __load_main_process_info(config_file: pd.ExcelFile) -> List[ScenarioConfig]:
        """メイン設定情報ロード

        シナリオ設定情報ファイルの「MAIN」シートから情報を読み込み、メイン設定情報として返却する

        Args:
            config_file (pd.ExcelFile): ホスト設定情報ファイル（pandasでExcelファイルを表すクラスのオブジェクト）

        Returns:
            maiConfigs: List[ScenarioConfig]: メイン設定情報 キーはシナリオ名
        """
        # 「MAIN」シート名設定
        config_sheet_name = 'MAIN'
        # 設定情報ファイルから「MAIN」シートの情報を読み込む
        main_collect_sheet = config_file.parse(config_sheet_name)
        # シナリオ設定情報辞書を初期化する
        mainConfigs: List[ScenarioConfig] = []
        # コマンド設定情報辞書を初期化する
        commandConfigs: List[CommandConfig] = []

        # MAINシートの行でループする
        for row in [AsciiFilter(row) for _, row in main_collect_sheet.iterrows()]:
            # MAINシートの行のシナリオ名がnullでない場合
            if not pd.isnull(row.SCENARIO):
                # 実行環境設定情報辞書を初期化する
                commandConfigs: List[CommandConfig] = []
                # シナリオ設定情報をMAINシートの行の情報と実行コマンド設定情報辞書で生成し、シナリオ設定情報辞書にシナリオ名"SCENARIO"をキーとして追加する
                mainConfigs.append(ScenarioConfig(row.SCENARIO, commandConfigs))
            
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
                commandConfigs.append(CommandConfig(row.NODE, row.ITEM, row.COMMAND, row.WHEN, 
                                                    row.CHECK_KIND, row.RESULT_OK, row.RESULT_NG, row.OPTION))
                if 'SUB' in row.COMMAND and sub_flg :
                    commandConfigs.append(sub_config)

        # 収集設定情報辞書を返却する
        return mainConfigs


    def __load_sub_process_info(sub_collect_sheet: pd.DataFrame, sub_sheet_name: str) -> List[ScenarioConfig]:
        """サブ設定情報ロード

        シナリオ設定情報ファイルの「SUB」シートから情報を読み込み、サブ設定情報として返却する

        Args:
            config_file (pd.ExcelFile): ホスト設定情報ファイル（pandasでExcelファイルを表すクラスのオブジェクト）

        Returns:
            subConfigs: List[ScenarioConfig]: サブ設定情報 キーはシナリオ名
        """
        # if sub_sheet_name == 'SUB001':
            # シナリオ設定情報辞書を初期化する
        subConfigs: List[ScenarioConfig] = []
        # コマンド設定情報辞書を初期化する
        commandConfigs: List[CommandConfig] = []

        # SUBシートの行でループする
        for row in [AsciiFilter(row) for _, row in sub_collect_sheet.iterrows()]:
            # SUBシートの行のシナリオ名がnullでない場合
            if not pd.isnull(row.SCENARIO):
                # 実行環境設定情報辞書を初期化する
                commandConfigs: List[CommandConfig] = []
                # シナリオ設定情報をSUB001シートの行の情報と実行コマンド設定情報辞書で生成し、シナリオ設定情報辞書にシナリオ名"SCENARIO"をキーとして追加する
                subConfigs.append(ScenarioConfig(row.SCENARIO, commandConfigs))

            # SUBシートの行の実行環境名がnullでない場合
            if not pd.isnull(row.NODE):
                # 実行コマンド設定情報をSUBシートの行の情報で生成し、実行コマンド設定情報辞書に実行コマンド項目名"ITEM"をキーとして追加する
                commandConfigs.append(CommandConfig(row.NODE, row.ITEM, row.COMMAND, row.WHEN, 
                                                    row.CHECK_KIND, row.RESULT_OK, row.RESULT_NG, row.OPTION))
        # 収集設定情報辞書を返却する
        return subConfigs


    def __load_connect_info(config_file: pd.ExcelFile) -> List[ConnectConfig]:
        """接続設定情報ロード

        シナリオ設定情報ファイルの「LIST001」シートから情報を読み込み、接続設定情報として返却する
        収集ホスト設定情報配下の接続設定情報はpriority、bastionの昇順でソートされる

        Args:
            config_file (pd.ExcelFile): ホスト設定情報ファイル（pandasでExcelファイルを表すオブジェクト）

        Returns:
            List[ConnectConfig]: 接続設定情報
        """
        # シナリオ設定情報ファイルから「LIST001」シートの情報を読み込む
        connect_sheet = config_file.parse('LIST001')
        # 接続設定情報リストを初期化する
        connectConfigs: List[ConnectConfig] = []
        # LIST001シートの行でループする
        for row in [AsciiFilter(row) for _, row in connect_sheet.iterrows()]:
            # LIST001シートの行のコマンド実行ホスト名"HOST"がnullでない場合
            if not pd.isnull(row.HOST):
                # LISTシートの行の情報から接続設定情報を生成し、接続設定情報リストに追加する
                connectConfigs.append(
                    ConnectConfig(row.HOST, row.DN, row.DS, row.IP, row.VER,
                                  row.REGION, row.DEL_FLG))
        return connectConfigs

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
    config_sheet_name = 'MAIN'
    config = Config(config_file_name)
    print(config._Config__mainConfigs[0]._ScenarioConfig__commandConfigs[2]._CommandConfig__item)
    # for val in config._Config__mainConfigs[0]._ScenarioConfig__commandConfigs:
    #     print(val)
    #     print()
    #     print()
    # dict = config.mainConfigs[0]
    # result = val.values()
    # print(type(config.mainConfigs))
    # print(config.connectConfigs[2])
    # print(config.mainConfigs)
    print()
    print()
    # print(config.__load_main_process_info)
    # print(config._Config__subConfigs)