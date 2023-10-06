from pythonosc.udp_client import SimpleUDPClient
from PresetBackup import CommandLineIO
from time import sleep

cmd = CommandLineIO.CommandLineIO


# connector=MidiWii.connector.Instance


class Sender:

    def __init__(self, port_send_to: int, address_destination: str) -> None:
        self.port_send_to = port_send_to
        self.osc_client = SimpleUDPClient(address_destination, port_send_to)
        self.path_osc_save_preset = '/rnbo/inst/0/presets/save'
        self.path_osc_set_param = '/rnbo/inst/0/params'

    def restore_presets(self, presets: dict):
        for preset_name, preset_params in presets.items():
            cmd.print_confirm(f'Setting values for preset: {preset_name}...')
            for param_setting in preset_params:
                if 'path' in param_setting.keys() and 'value' in param_setting.keys():
                    self.osc_client.send_message(f'{self.path_osc_set_param}{param_setting["path"]}', param_setting["value"])
                else:
                    print('Skipping incorrectly formatted entry:\n', param_setting)
                sleep(0.01)
            cmd.print_confirm(f'Saving preset as: {preset_name}\n')
            self.osc_client.send_message(f'{self.path_osc_save_preset}', preset_name)
            sleep(.3)