import os, shutil

# Test the defolder capabilities with custom files
def test_defolder():
    path = r"C:\Temporal\sandbox\test"
    result_files = [
        "file1",
        "file2",
        "file3",
        "folder1-file11",
        "folder1-folder11-file111",
        "folder2-file21",
        "folder3-file31",
    ]

    # Create the test sandbox
    shutil.copytree(r".\tests\template", path)

    # Run the file and get the result
    os.system("py main.py -s " + path)
    files = list([e.name for e in os.scandir(path)])

    # Remove trail
    shutil.rmtree(path)

    assert files == result_files


# Same test changing the folder name to False
def test_defolder_no_folder_name():
    path = r"C:\Temporal\sandbox\test"
    result_files = [
        "file1",
        "file11",
        "file111",
        "file2",
        "file21",
        "file3",
        "file31",
    ]

    # Create the test sandbox
    shutil.copytree(r".\tests\template", path)

    # Run the file and get the result
    os.system("py main.py --no-folder-name -s " + path)
    files = list([e.name for e in os.scandir(path)])

    # Remove trail
    shutil.rmtree(path)

    assert files == result_files


# Original test changing the separator
def test_defolder_different_separator():
    path = r"C:\Temporal\sandbox\test"
    result_files = [
        "file1",
        "file2",
        "file3",
        "folder1_file11",
        "folder1_folder11_file111",
        "folder2_file21",
        "folder3_file31",
    ]

    # Create the test sandbox
    shutil.copytree(r".\tests\template", path)

    # Run the file and get the result
    os.system("py main.py --separator _ -s " + path)
    files = list([e.name for e in os.scandir(path)])

    # Remove trail
    shutil.rmtree(path)

    assert files == result_files
