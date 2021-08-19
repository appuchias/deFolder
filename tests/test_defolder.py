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
