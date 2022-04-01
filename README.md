# Avid-Log-Exchange-Table
A table GUI using PySide2 to import manipulate and save Avid Log Exchange files.
To my knowledge, Avid Log Exchange files can't be open on any table application or can be corrupted that way.
You can build it if you've installed pyinstaller 
``
$ pip install pyinstaller
``
and use the build.sh
``
$ chmod +x build.sh
$ ./build.sh
``

## Hidden functions
Drag and drop to import an ALE file to the table.
You can copy a single cell (CMD + C) and paste (CMD + V) it to multiples cells or copy multiples cells.
Only tested in MacOS.

## Requirements
PySide2
