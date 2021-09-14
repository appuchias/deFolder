import os, shutil, stat, errno
import main

# Empty test directory
path = "C:\\Temporal\\sandbox\\test\\"


def empty_test_directory():
    try:
        shutil.rmtree(path, ignore_errors=False, onerror=handleRemoveReadonly)
    except PermissionError:
        print(list(os.listdir(path)))
        raise


def handleRemoveReadonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise


def check_dir_validity(
    src_dir: str, comparelist: list = None, remove_trail: bool = False
) -> bool:
    assert os.path.exists(src_dir)

    if not comparelist:
        comparelist = [
            "file1",
            "file2",
            "file3",
            "folder1",
            "folder2",
            "folder3",
        ]

    src_list = [e.name for e in os.scandir(src_dir)]

    # Remove trail
    if remove_trail:
        empty_test_directory()

    return src_list == comparelist


# Test the defolder capabilities with custom files
def test_defolder():
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
    try:
        shutil.copytree(".\\tests\\template", path)
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    except FileExistsError:
        empty_test_directory()
        shutil.copytree(".\\tests\\template", path)
    assert check_dir_validity(path)

    assert True

    # Run the file and get the result
    os.system("py main.py -q " + path)

    assert check_dir_validity(path, result_files, remove_trail=True)


# Same test changing the folder name to False
def test_defolder_no_folder_name():
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
    try:
        shutil.copytree(".\\tests\\template", path)
    except FileExistsError:
        empty_test_directory()
        shutil.copytree(".\\tests\\template", path)
    assert check_dir_validity(path)

    # Run the file and get the result
    os.system("py main.py --no-folder-name -q " + path)

    assert check_dir_validity(path, result_files, remove_trail=True)


# Original test changing the separator
def test_defolder_different_separator():
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
    try:
        shutil.copytree(".\\tests\\template", path)
    except FileExistsError:
        empty_test_directory()
        shutil.copytree(".\\tests\\template", path)
    assert check_dir_validity(path)

    # Run the file and get the result
    os.system("py main.py -s _ -q " + path)

    assert check_dir_validity(path, result_files, remove_trail=True)


# Should jump out of the try block
def test_verbosity_group():
    try:
        os.system("py main.py -q -v")
        assert False
    except:
        assert True


# Should raise an exception
def test_folder_name_group():
    try:
        os.system("py main.py --no-folder-name -s _")
        assert False
    except:
        assert True


if __name__ == "__main__":
    test_defolder()
