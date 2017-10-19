# Botw-AutoMipping
<img src="https://img.shields.io/badge/Python-3.5%2B-yellow.svg"> [<img src="https://img.shields.io/badge/Support-me!-orange.svg">](https://www.patreon.com/Ainz)

A automatic mip-disabling tool for bfres files in Zelda: Breath of the Wild.

Simply drag the script and the bfres model you want to modify into command line and it will do its magic. Note that if you don't put a space between the program and the bfres file it won't work.

>C:\Location_Of_Folder\> BOTW-AutoMips.py Model_File.bfres

If you have trouble using this tool on a windows system, there is a possibility that your registry is preventing you from using python scripts in the command line.

Modifying the following two registries so that the arguments are passed along to Python:

> HKEY_CLASSES_ROOT\Applications\python.exe\shell\open\command

> HKEY_CLASSES_ROOT\py_auto_file\shell\open\command

Add %* to the existing "C:\PythonXX\python.exe" "%1", so that the key now looks like: "C:\PythonXX\python.exe" "%1" %*.
