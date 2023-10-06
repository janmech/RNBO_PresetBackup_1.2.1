import os
import json
import random
import string
from pathlib import Path
import traceback
from PresetBackup import BashColors
from PresetBackup import CommandLineIO

Cmb = CommandLineIO.CommandLineIO
Color = BashColors.Color


class Writer:
    def __init__(self) -> None:
        pass

    @staticmethod
    def write_backup_file(backup_presets: dict, patcher_name: str, suffix: str = '') -> bool:
        save_path = '/home/pi/Documents/rnbo-presets'
        if Path(save_path).is_dir() is False:
            os.mkdir(save_path)
        patcher_name = patcher_name.replace(' ', '-')
        suffix = suffix.replace(' ', '-')
        if suffix == 'rnd':
            suffix = f'--{Writer.get_random_string()}'
        elif suffix != '':
            suffix = f'--{suffix}'
        file_path = f'{save_path}/presets-{patcher_name}{suffix}.json'

        if os.path.isfile(file_path):
            answer = input(f'{Color.FAIL}The file {file_path} already exists. Replace file?{Color.ENDC}  [y/n] ').lower()
            if answer != 'y':
                return False
        try:
            with open(file_path, 'w') as fp:
                json.dump(
                    backup_presets,
                    fp,
                    sort_keys=True,
                    indent=4,
                )
            return True
        except Exception:
            traceback.print_last()
            return False

    @staticmethod
    def get_random_string() -> str:
        rnd_str_elements = string.digits
        rnd_str = ''.join(random.choice(rnd_str_elements) for i in range(6))
        rnd_str = rnd_str + '-' + ''.join(random.choice(rnd_str_elements) for i in range(6))
        return rnd_str
