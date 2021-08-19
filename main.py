import os, argparse
from os import path, walk
from pathlib import Path


# Checks if there is a folder inside the specified path
def is_there_a_folder(src_path: str) -> bool:
    assert path.exists(src_path), "Provided path does not exist."
    for element in os.scandir(src_path):
        if element.is_dir():
            break
    else:
        return False
    return True


# Removes folders recurrsively moving files upwards in the directory tree. Returns false if no folders were removed
def recursive_child_remover(src_path: Path) -> bool:
    assert path.exists(src_path), "Provided path does not exist."
    parent = src_path.parent

    # while is_there_a_folder(src_path):
    #     for element in os.scandir(src_path):
    #         if element.is_dir():
    #             recursive_child_remover(Path(element.path))
    #         elif element.is_file():
    #             dest_path = path.join(parent, element.name)

    #             if args.verbose:
    #                 print(
    #                     element.path,
    #                     "→",
    #                     path.join(dest_path, str(src_path) + "-" + element.name),
    #                 )

    #             os.rename(
    #                 element.path,
    #                 path.join(dest_path, str(src_path) + "-" + element.name),
    #             )
    # os.rmdir(src_path)

    # While added to repeat the loop in consecutive folders
    while is_there_a_folder(src_path):

        # Cycle through all the files in each folder
        for root, _, files in os.walk(src_path):

            # Avoid moving files in the root folder
            if Path(root) != src_path:
                for element in files:

                    # Get the file path as a path object
                    file_path = Path(path.join(root, element))

                    # Move the file itself
                    os.rename(
                        file_path,
                        path.join(src_path, str(file_path.parent) + "-" + element),
                    )

                    # UX
                    print(
                        file_path,
                        "->",
                        path.join(src_path, str(file_path.parent) + "-" + element),
                    )

        # 'If' to avoid removing root folder, remove every other child folder
        if Path(root) != src_path:
            os.rmdir(root)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "src_folder",
        help="Folder to sort through",
        metavar="source folder",
        type=Path,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Only print changes, do not move files",
        action="store_true",
    )

    args = parser.parse_args()

    src_folder = Path(path.abspath(args.src_folder))

    recursive_child_remover(src_folder)

    print("Done")
