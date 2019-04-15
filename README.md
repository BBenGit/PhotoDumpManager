# PhotoDumpManager

PhotoDumpaManager is a tool that sis designed for photographers but is usefull in more domains. 
It sorts a dump directory (e.g. camera SD card) to an ordered exit directory.

# How to install

## Prerequisite

You will need python3 to use this script. Please refer to the official website : https://www.python.org/download/releases/3.0/.

## Getting the script

```
curl -o /usr/local/bin/pdm https://github.com/BBenGit/PhotoDumpManager/blob/master/PhotoDumpManager.py
chmod +x /usr/local/bin/pdm
```

# How to use

You can now use the command pdm to order your files. Both `<input_directory> <output_directory>` must exist before using the `pdm` command.
```bash
USAGE:
        pdm <input_directory> <output_directory>
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

