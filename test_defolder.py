import os, shutil, stat, errno
import main, pytest

# Empty test directory
path = "C:\\Temporal\\sandbox\\test\\"


def handleRemoveReadonly(func, path, exc):
    if func in (os.rmdir, os.remove) and exc[1].errno == errno.EACCES:
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
        shutil.rmtree(path, ignore_errors=False, onerror=handleRemoveReadonly)

    return sorted(src_list) == sorted(comparelist)


# Test the defolder capabilities with custom files and all possibilities
@pytest.mark.parametrize(
    ("src_path", "is_verbose", "separator", "folder_name"),
    (
        (path, True, "-", True),
        (path, True, "-", False),
        (path, True, "_", True),
        (path, False, "-", True),
        (path, False, "-", False),
        (path, False, "_", True),
        (path, False, None, True),
        (path, False, None, False),
    ),
)
def test_defolder(src_path: str, is_verbose: bool, separator: str, folder_name: bool):
    if folder_name:
        result_files = [
            "file1",
            "file2",
            "file3",
            f"folder1{separator if separator else '-'}file11",
            f"folder1{separator if separator else '-'}folder11{separator if separator else '-'}file111",
            f"folder2{separator if separator else '-'}file21",
            f"folder3{separator if separator else '-'}file31",
        ]
    else:
        result_files = [
            "file1",
            "file2",
            "file3",
            f"file11",
            f"file111",
            f"file21",
            f"file31",
        ]

    # Create the test sandbox
    try:
        shutil.copytree(".\\test", path)
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    except FileExistsError:
        shutil.rmtree(path, ignore_errors=False, onerror=handleRemoveReadonly)
        shutil.copytree(".\\test", path)

    # Ensure all files were copied successfully
    assert check_dir_validity(path)

    # Run the file and check for in-function validation
    main.defolder(src_path, is_verbose, separator, folder_name)

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
