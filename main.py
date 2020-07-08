import os

with open("paths.txt") as r:
    source = r.readlines()[0]
    dest = r.readlines()[1]

for root, subfolders, files in os.walk(source):
    root_list = root.split("\\")
    folder = root_list[-1:][0]
    for file in files:
        os.rename(f'{root}/{file}', f'{dest}/{folder}-{file}')
    print(folder)

print("Program finished!")
