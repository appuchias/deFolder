# deFolder

[![MIT license](https://img.shields.io/github/license/appuchias/deFolder?style=flat-square)](https://github.com/appuchias/deFolder/blob/master/LICENSE)
[![Author](https://img.shields.io/badge/Project%20by-Appu-9cf?style=flat-square)](https://github.com/appuchias)
![Size](https://img.shields.io/github/repo-size/appuchias/deFolder?color=orange&style=flat-square)

## How it works

This will move all files in subfolders to their root folder. Using `os.walk` it will cycle every child folder recursively and if files are found, move them to the parent folder, prepending the folder name to the file name.

## Setup

Fist of all, you need some path to 'deFolder' so this can take effect. At least one subfolder is needed and every action the script does can be easily changed to your needs.

To set this repo up, you'll need to open the terminal and type:

 1. Navigate to the path where you want the repo: `cd <path>`
 1. Clone the repo: `git clone https://github.com/appuchias/deFolder.git`
 1. Navigate inside the repo folder: `cd deFolder`
 1. From the terminal, run the file: `python main.py [-h] [-v] [-s] <source_folder>`
 1. For more information about usage, run `python main.py -h`

## License

This project is licensed under the [MIT license](https://github.com/appuchias/deFolder/blob/master/LICENSE).

Coded with 🖤 by Appu
