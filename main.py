import os
from os import path
import sys

try:
    with open("paths.txt") as r:
        source = r.readlines()[0]
        dest = r.readlines()[1]
except:
    try:
        source = sys.argv[1]
        dest = sys.argv[2]
    except:
        print("Provide paths either though the file or the CL")

for root, subfolders, files in os.walk(source):
    folder = path.split(root)[
        1
    ]  # 'split("c:/dir")' returns '("c:/", "dir")' so I take the directory
    for file in files:
        os.rename(f"{root}/{file}", f"{dest}/{folder}-{file}")
    print(folder)

print("Program finished!")
