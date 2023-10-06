# RNBO Preset Backup

## Synopsis


Working on larger projects with RNBO and the Raspberry Pi I frequently encountered the situation that I already had created various presets on the Pi and then needed to update the patcher for minor fixes or improvements. In other moments I accedentially have overwritten a preset.

In those cases the presets created directly on the Raspberry Pi were lost.

RNBO Preset Backup is a python programm for these situation:

A tool for managing presets on a Raspberry Pi Running a [Cycling'74 RNBO Patcher](https://rnbo.cycling74.com)
It allows to backup prestes from the loaded patcher to a JSON file and restore them later.

# System requirements
- A Raspberry Pi running RNBO 1.2.1 or later
- Python 3.9 or later

## Installing
- ssh into your Raspberry Pi running RNBO
- change to your *Documents* folder with the command:  
`cd ~/Documents`
- clone this repository using https:  
  `git clone https://github.com/janmech/RNBO_PresetBackup_1.2.1.git`
- cd into the newly created folder *RNBO_PresetBackup_1.2.1*:
  `cd RNBO_PresetBackup_1.2.1`
- run the setup script:  
`python setup.py`

This script will install the dependencies. (the python package [python-osc](https://pypi.org/project/python-osc/)) and create links to the *rnbo-presets-backup.py* and *rnbo-presets-restore.py* scrips so thay can be used like regular shell commands.

## Uninstalling

- remove the folder RNBO_PresetBackup_1.2.1: `rm -r path/to/RNBO_PresetBackup_1.2.1`
- delete the links in */usr/local/bin*:  
`sudo unlink /usr/local/bin/rnbo-presets-backup.py` and  
`sudo unlink /usr/local/bin/rnbo-presets-restore.py`

## Usage

### Backing up prestes:
rnbo-presets-backup [OPTION] [FILE]...

> Backup presets from currently loaded RNBO patch.

options:  
> -h, --help            show this help message and exit  
> -s SUFFIX, --suffix SUFFIX
                        Filename suffix. Use '-s rnd' for a random string

The backup file will be stored under: `/home/pi/Documents/rnbo-presets` in a file name following the pattern `presets-[patcher-name][--suffix].json`

If you want to have a safety copy of your backuped presets simply copy the files in `/home/pi/Documents/rnbo-presets` to another location.

### Restoring prestes:
rnbo-presets-restore [OPTION] 

> Restore RNBO Presets from backup file

optional arguments:
> -h, --help  show this help message and exit

The script will guide you through the steps

### How backups are restored:
The mechanism is really simple. The script sets the parameters to the stored values and saves a preset ander the stored preset name.


