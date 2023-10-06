#!/usr/bin/env python3
# coding=utf-8

import os

print('\033[93m ->Installing dependencies...\033[0m')
os.system("pip install python-osc")
print('\033[93m ->Installing dependencies: done!\n\033[0m')

print("\033[93m ->Linking scripts to /usr/local/bin...\033[0m")
print("\033[93m -You will we asked for your password.\033[0m")
os.system("sudo -K")
os.system("sudo -v")


if os.path.isfile('/usr/local/bin/rnbo-presets-backup'):
    os.system("sudo unlink /usr/local/bin/rnbo-presets-backup")
os.system(f'sudo ln -s {os.path.abspath("./rnbo-presets-backup.py")} /usr/local/bin/rnbo-presets-backup')

if os.path.isfile('/usr/local/bin/rnbo-presets-restore'):
    os.system("sudo unlink /usr/local/bin/rnbo-presets-restore")
os.system(f'sudo ln -s {os.path.abspath("./rnbo-presets-restore.py")} /usr/local/bin/rnbo-presets-restore')
print("\033[93m ->Linking scripts: done!\033[0m")




