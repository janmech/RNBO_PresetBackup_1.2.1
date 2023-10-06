#!/usr/bin/env python3
# coding=utf-8
from __future__ import annotations

import sys
import traceback
import argparse
from argparse import ArgumentParser
from PresetBackup import CommandLineIO
from PresetBackup import Sqlite
from PresetBackup import BackUp as Ba

cmd_io = CommandLineIO.CommandLineIO


def init_argparse() -> argparse.ArgumentParser:
    arg_parser: ArgumentParser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Backup presets from currently loaded RNBO patch."
    )
    arg_parser.add_argument("-s", "--suffix", help="Filename suffix. Use '-s rnd' for a random string", required=False, default='')
    arg_parser.add_argument("-t", "--test", help="Use Test File Path", required=False, default=False,  action='store_true',)
    return arg_parser


if __name__ == '__main__':
    try:
        parser = init_argparse()
        args = parser.parse_args()
        try:
            rnbo_ids = cmd_io.get_rnbo_ids(args.test)
            if rnbo_ids is None:
                exit(0)
            db_connector = Sqlite.Connector()
            patcher_id = db_connector.get_patcher_id(rnbo_ids, args.test)
            if patcher_id is None:
                exit(0)
            patcher_name = db_connector.get_patcher_name(patcher_id, args.test)
            backup_presets = db_connector.get_backup_presets(patcher_id, args.test)
            if backup_presets is None:
                exit(0)
            Ba.Writer.write_backup_file(backup_presets, patcher_name, args.suffix, args.test)
        except FileNotFoundError:
            traceback.print_last()
            traceback.print_stack()
    except KeyboardInterrupt:
        print()
        sys.exit(0)
