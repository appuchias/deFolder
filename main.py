import os

source = "D:/WALL"
dest = "D:/WALL"

for root, subfolders, files in os.walk(source):
    root_list = root.split("\\")
    folder = root_list[-1:][0]
    for file in files:
        os.rename(f'{root}/{file}', f'{dest}/{folder}-{file}')
    print(folder)
