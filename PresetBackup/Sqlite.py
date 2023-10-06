from __future__ import annotations

import sqlite3
from PresetBackup import CommandLineIO as Cmd


class Connector:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_patcher_id(rnbo_ids: tuple) -> int | None:
        db_path = '/home/pi/Documents/rnbo'
        connection = sqlite3.connect(f'{db_path}/oscqueryrunner.sqlite')
        cursor = connection.cursor()
        (config_id, runner_id) = rnbo_ids
        result = cursor.execute(
            f"SELECT `id` FROM patchers WHERE `config_path` LIKE '%{config_id}%' AND `so_path` LIKE '%{runner_id}%'").fetchall()
        if len(result) != 1:
            Cmd.CommandLineIO.print_notice("No presets found in database for loaded patches.\nPlease create presets before running this backup script.")
            return None
        connection.close()
        return result[0][0]

    @staticmethod
    def get_patcher_name(patcher_id: int, is_test: bool = False) -> str | None:
        if is_test:
            db_path = './TestData'
        else:
            db_path = '/home/pi/Documents/rnbo'
        connection = sqlite3.connect(f'{db_path}/oscqueryrunner.sqlite')
        cursor = connection.cursor()
        result = cursor.execute(f"SELECT `name` FROM patchers WHERE `id` = {patcher_id}").fetchone()
        if result is not None:
            return result[0]
        return None

    @staticmethod
    def get_backup_presets(patcher_id: int, is_test: bool = False) -> dict:
        if is_test:
            db_path = './TestData'
        else:
            db_path = '/home/pi/Documents/rnbo'
        connection = sqlite3.connect(f'{db_path}/oscqueryrunner.sqlite')
        cursor = connection.cursor()
        result = cursor.execute(f"SELECT * FROM presets WHERE `patcher_id` = {patcher_id}").fetchall()
        return Cmd.CommandLineIO.print_db_presets_result(result)
