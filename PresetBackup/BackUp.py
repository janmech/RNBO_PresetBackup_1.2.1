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
    def extract_params(preset_dict: dict, param_list=None, path_prefix=None) -> list:
        try:
            if param_list is None:
                param_list = []
            if path_prefix is None:
                path_prefix = ''

            if param_list is None:
                param_list = []
            for path_atom_0 in preset_dict:
                atom_0_value = preset_dict[path_atom_0]
                if type(atom_0_value) is dict:
                    if 'value' in atom_0_value.keys():
                        path = path_prefix + '/' + path_atom_0
                        path = path.replace('/__sps', '')
                        value = atom_0_value['value']
                        param_list.append(
                            {
                                'path': path,
                                'value': value
                            }
                        )
                    else:
                        Writer.extract_params(preset_dict[path_atom_0], param_list, path_prefix + '/' + path_atom_0)
        except Exception as e:
            print("Error Reading File")
            traceback.print_exc()

        return param_list

    @staticmethod
    def write_backup_file(backup_presets: dict, patcher_name: str, suffix: str = '', is_test: bool = False) -> bool:
        if is_test:
            save_path = './rnbo-presets'
        else:
            save_path = '/home/pi/Documents/rnbo-presets'
        extracted_params = {}
        for preset_name, preset_data in backup_presets.items():
            extracted_params[preset_name] = Writer.extract_params(preset_data)
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
                    extracted_params,
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
