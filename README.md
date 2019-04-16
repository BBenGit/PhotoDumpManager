# PhotoDumpManager

`PhotoDumpManager` is a tool that is designed for photographers but is useful in more domains. 
It sorts an input directory (e.g. camera SD card) to an ordered output directory.

# How to install

## Prerequisite

You will need `python3` (*> 3.4*) to use this script. Please refer to the [official Python website](https://www.python.org/download/releases/3.4/) for more information. 

## Getting the script

```
curl -o /usr/local/bin/pdm https://raw.githubusercontent.com/BBenGit/PhotoDumpManager/master/PhotoDumpManager.py && chmod +x /usr/local/bin/pdm
```

# How to use

You can now use the pdm `command` to order your files. `input` has to exist on the filesystem before calling `pdm`.
```bash
usage: PhotoDumpManager.py [-h] [--recursive] --input-directory
                           INPUT_DIRECTORY --output-directory OUTPUT_DIRECTORY
                           --types TYPES [TYPES ...]

optional arguments:
  -h, --help            show this help message and exit
  --recursive, -r
  --input-directory INPUT_DIRECTORY, -i INPUT_DIRECTORY
                        Directory where to find input images
  --output-directory OUTPUT_DIRECTORY, -o OUTPUT_DIRECTORY
                        Directory where to put destination files
  --types TYPES [TYPES ...], -t TYPES [TYPES ...]
                        Types of file to be ordered
```

## Example

```bash
pdm -i /media/SDcard/DCIM -o ~/Pictures
```

The file structure is as folowing :
```
Pictures    
└───Type
  └───Year
    └───Month
      └───Day
```
e.g.
```
Pictures    
└─RAW
│ └─2019
│   └─March
│   │ └─24
│   │ └─28
│   └─April
│     └─02
│     └─18
└─JPG
  └─2019
    └─March
  │   └─24
  │   └─28
...
```

