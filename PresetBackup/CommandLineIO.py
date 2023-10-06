from __future__ import annotations
import json
import os
from datetime import datetime
from typing import Union
from json.decoder import JSONDecodeError
from PresetBackup import BashColors

Color = BashColors.Color


class CommandLineIO:

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_rnbo_ids() -> tuple | None:
        rnbo_ids = None
        last_path = '/home/pi/Documents/rnbo/saves'
        file_candidates = []
        files = os.listdir(last_path)
        for file in files:
            if file.startswith('last-') and file.endswith('.json'):
                file_candidates.append(file)
        if len(file_candidates) > 1:
            while True:
                chosen_config_file = CommandLineIO.choose_input_config_file(file_candidates)
                if chosen_config_file == 'x':
                    return None
                if chosen_config_file is None:
                    CommandLineIO.print_notice('Invalid choice. Try again\n')
                    continue
                rnbo_ids = CommandLineIO.parse_last_config_file(last_path, chosen_config_file)
                break
            if rnbo_ids is None:
                CommandLineIO.print_error('Error parsing last config file.')
                return None
        else:
            chosen_config_file = file_candidates[0]
            rnbo_ids = CommandLineIO.parse_last_config_file(last_path, chosen_config_file)

        return rnbo_ids

    @staticmethod
    def choose_input_config_file(file_candidate: list) -> str | None:
        CommandLineIO.print_regular("More than one possible config file found:")
        for i in range(0, len(file_candidate)):
            print(f'\t[{i}]\t {file_candidate[i]}')
        print(f'\t[x]\t exit')

        try:
            answer = input(f'{Color.WARNING}Which file would you like to use? {Color.ENDC}').lower()
            if answer == 'x':
                return answer
            answer = int(answer)
        except ValueError:
            return None
        if not 0 <= answer <= len(file_candidate):
            return None
        return file_candidate[answer]

    @staticmethod
    def choose_input_preset_file() -> str | None:
        chosen_file = None
        path = "/home/pi/Documents/rnbo-presets"

        file_candidates = []
        files = os.listdir(path)
        for file in files:
            if file.startswith('presets-') and file.endswith('.json'):
                file_candidates.append((file, str(datetime.fromtimestamp(os.path.getctime(f'{path}/{file}')))))

        if len(file_candidates) == 0:
            CommandLineIO.print_notice(f'No preset backup files found in {os.path.abspath(path)}')
            CommandLineIO.print_notice(f'Backup presets before restoring')
            return None
        while True:
            CommandLineIO.print_regular(f'Found those preset backup files: ')
            print(f'{"".ljust(7)}{"File Name".ljust(50)}{"Last Modified"}')
            i = 0
            for file_name, modified in file_candidates:
                print(f'{f"[{i}]".ljust(7)}{file_name.ljust(50)}{modified}')
                i = i + 1
            print(f'{f"[x]".ljust(7)}exit')
            answer = input(f'{Color.WARNING}Which file would you like to use?{Color.ENDC} ')
            if answer.lower() == 'x':
                return chosen_file
            else:
                try:
                    answer = int(answer)
                    if 0 <= answer < i:
                        chosen_file = answer
                        break
                except ValueError:
                    CommandLineIO.print_notice('Invalid choice. Try again\n')

        return f'{os.path.abspath(path)}/{file_candidates[answer][0]}'

    @staticmethod
    def choose_restore_presets(presets: dict) -> dict | None:
        CommandLineIO.print_regular('\nThe selected file contains the following presets:')
        i = 0
        print(f'{"".ljust(7)}{"Preset Name".ljust(50)}')
        for preset_name in presets.keys():
            print(f'{f"[{i}]".ljust(7)}{preset_name.ljust(50)}')
            i = i + 1
        print(f'{f"[all]".ljust(7)}all presets')
        while True:
            valid_choices = {}
            answer = input(f'{Color.WARNING}Select Presets to restore (comma separated): {Color.ENDC}')
            if answer.lower() == 'all':
                valid_choices = presets
                break
            selected_presets = answer.split(',')
            presets_names_list = list(presets.keys())
            for selected_preset in selected_presets:
                try:
                    selected_preset = int(selected_preset)
                    if 0 <= selected_preset < len(presets.keys()):
                        valid_choices[presets_names_list[selected_preset]] = presets[presets_names_list[selected_preset]]
                except ValueError:
                    continue
            if len(valid_choices) > 0:
                break
            CommandLineIO.print_notice("Invalid choice. Try again.\n")
        valid_choices_keys = list(valid_choices.keys())
        valid_choices_keys.sort()
        valid_choices = {i: valid_choices[i] for i in valid_choices_keys}
        CommandLineIO.print_regular('\nThe following presets will be restored:')
        for key in valid_choices.keys():
            print(f'{key.ljust(50)}')
        if input(f'{Color.OKCYAN}Please confirm {Color.ENDC}[y/n]: ').lower() != 'y':
            return None
        return valid_choices

    @staticmethod
    def parse_last_config_file(path: str, file_name: str) -> tuple | None:
        try:
            config_id = None
            runner_id = None
            with open(f'{path}/{file_name}') as f:
                last_config_dict = json.load(f)

            if 'instances' in last_config_dict and 'config_path' in last_config_dict['instances'][0]:
                config_id = last_config_dict['instances'][0]['config_path']
                config_id = config_id[config_id.rindex('rnbogen.') + 8:config_id.rindex('-config.json')]

            if 'instances' in last_config_dict and 'so_path' in last_config_dict['instances'][0]:
                runner_id = last_config_dict['instances'][0]['so_path']
                runner_id = runner_id[runner_id.rindex('libRNBORunnerSO') + 8:runner_id.rindex('.so')]
            if config_id is not None and runner_id is not None:
                return config_id, runner_id
            else:
                raise ValueError
        except ValueError:
            CommandLineIO.print_error('Error parsing last config \n')
            return None
        except FileNotFoundError:
            CommandLineIO.print_error('Error opening last config \n')
            return None

    @staticmethod
    def parse_preset_file(preset_file: str) -> dict | None:
        try:
            with open(preset_file) as json_file:
                presets = json.load(json_file)
        except Union[FileNotFoundError, JSONDecodeError]:
            return None
        return presets

    @staticmethod
    def print_db_presets_result(presets: list) -> dict:
        if len(presets) == 0:
            CommandLineIO.print_notice(f'No presets found for patcher')
        else:
            preset_data = {}
            backup_presets = {}
            for preset in presets:
                preset_data[preset[2]] = preset[3]
            CommandLineIO.print_regular(f'Found {len(presets)} preset(s):')
            i = 0
            print(f'{"Index":8}Preset Name')
            for preset in presets:
                selector = f'[{i}]'
                print(f'{selector:8}{preset[2]}')
                i = i + 1
            print(f'{"[all]":8}Backup all Presets')
            chosen_presets = input(f'{Color.WARNING}Select presets to back up (comma separated): {Color.ENDC}')
            if chosen_presets.lower() == 'all':
                confirmation = input(
                    f'{Color.OKCYAN}Please confirm: Back up ALL presets?{Color.ENDC} [y/n]: ').lower() == 'y'
                if confirmation:
                    backup_presets = preset_data
            else:
                valid_choices = []
                chosen_presets = chosen_presets.split(',')
                for i in chosen_presets:
                    try:
                        preset_index = int(i)
                        if 0 <= preset_index < len(presets):
                            valid_choices.append(preset_index)
                    except ValueError:
                        pass
                valid_choices = list(dict.fromkeys(valid_choices))
                valid_choices.sort()
                if len(valid_choices) == 0:
                    CommandLineIO.print_notice(f'Invalid Choice. Try again\n')
                    CommandLineIO.print_db_presets_result(presets)
                else:
                    CommandLineIO.print_regular(f'Back up the following presets:')
                    print(f'{"Index":8}Preset Name')
                    for i in valid_choices:
                        selector = f'[{i}]'
                        print(f'{selector:8}{presets[i][2]}')
                    confirmation = input(f'{Color.OKCYAN}Please confirm{Color.ENDC} [y/n]: ').lower() == 'y'
                    if confirmation:
                        backup_presets = {}
                        preset_data_list = list(preset_data.items())
                        for i in valid_choices:
                            backup_presets[preset_data_list[i][0]] = preset_data_list[i][1]
            for preset_name in backup_presets.keys():
                backup_presets[preset_name] = json.loads(backup_presets[preset_name])
            return backup_presets

    @staticmethod
    def print_error(message: str) -> None:
        print(f'{Color.FAIL}{message}{Color.ENDC}')

    @staticmethod
    def print_notice(message: str) -> None:
        print(f'{Color.OKCYAN}{message}{Color.ENDC}')

    @staticmethod
    def print_regular(message: str) -> None:
        print(f'{Color.WARNING}{message}{Color.ENDC}')

    @staticmethod
    def print_confirm(message: str)->None:
        print(f'{Color.OKGREEN}{message}{Color.ENDC}')
