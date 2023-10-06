#!/usr/bin/env python3
# coding=utf-8
from __future__ import annotations
from argparse import ArgumentParser as ArgumentParser
from PresetBackup import OscSender
from PresetBackup import CommandLineIO

cmd_io = CommandLineIO.CommandLineIO


def init_argparse() -> ArgumentParser:
    arg_parser: ArgumentParser = ArgumentParser(
        usage="%(prog)s [OPTION] ",
        description="Restore RNBO Presets from backup file"
    )
    return arg_parser


if __name__ == '__main__':
    try:
        parser = init_argparse()
        args = parser.parse_args()
        osc_sender = OscSender.Sender(1234, '127.0.0.1')
        preset_file: str | None = cmd_io.choose_input_preset_file()
        if preset_file is None:
            exit(0)
        presets: dict | None = cmd_io.parse_preset_file(preset_file)
        if presets is None or len(presets) == 0:
            cmd_io.print_error('No presets found in file.')
            exit(1)
        selected_presets = cmd_io.choose_restore_presets(presets)
        if selected_presets is None:
            exit(0)
        osc_sender.restore_presets(selected_presets)
    except KeyboardInterrupt:
        print()
        exit(0)
