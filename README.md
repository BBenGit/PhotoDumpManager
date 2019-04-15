# PhotoDumpManager

PhotoDumpaManager is a tool that sis designed for photographers but is usefull in more domains. 
It sorts a dump directory (e.g. camera SD card) to an ordered exit directory.

# How to install

## Prerequisite

You will need python3 to use this script. Please refer to the official website : https://www.python.org/download/releases/3.0/.

## Getting the script

```
curl -o /usr/local/bin/pdm https://raw.githubusercontent.com/BBenGit/PhotoDumpManager/master/PhotoDumpManager.py
chmod +x /usr/local/bin/pdm
```

# How to use

You can now use the pdm `command` to order your files. Both `input` and `output` directories have to exist on filesystem before calling `pdm`.
```bash
usage: pdm [-h] --input-directory INPUT_DIRECTORY
                --output-directory OUTPUT_DIRECTORY

optional arguments:
  -h, --help            show this help message and exit
  --input-directory INPUT_DIRECTORY, -i INPUT_DIRECTORY
                        Directory where to find input images
  --output-directory OUTPUT_DIRECTORY, -o OUTPUT_DIRECTORY
                        Directory where to put destination files
```

## Example

```bash
        pdm /media/SDcard/DCIM ~/Pictures
```

The file structure is as folowing :
```
Pictures    
│
└───Type
    │
    └───Year
        │
        └───Month
            │
            └───Day
```
e.g.
```
Pictures    
│
└───RAW
│    │
│    └───2019
│        │
│        └───March
│        │   │
│        │   └───24
│        │   │
│        │   └───28
│        │
│        └───April
│            │
│            └───02
│            │
│            └───18
└───JPG
    │
    └───2019
        │
        └───March
        │   │
        │   └───24
        │   │
        │   └───28

...
```

