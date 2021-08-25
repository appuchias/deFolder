import os, argparse
from os import path, walk
from pathlib import Path


# Checks if there is a folder inside the specified path
def is_there_a_folder(src_path: str) -> bool:
    assert path.exists(src_path), "Provided path does not exist."

    # If there is a folder, break the loop and return True
    for element in os.scandir(src_path):
        if element.is_dir():
            break

    else:
        return False

    return True


# Removes folders recurrsively moving files upwards in the directory tree. Returns False if no folders were deleted
def remove_child_folders(
    src_path: Path, is_verbose: bool, separator: str, folder_name: bool = True
) -> bool:

    assert path.exists(src_path), "Provided path does not exist."
    result = False

    # Print info
    if is_verbose:
        print("Running deFolder in", src_path)

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
                        path.join(
                            src_path,
                            (
                                (str(file_path.parent) + str(separator))
                                if folder_name
                                else ""
                            )
                            + element,
                        ),
                    )

                    # UX
                    if is_verbose:
                        print(
                            file_path,
                            "->",
                            path.join(src_path, str(file_path.parent) + "-" + element),
                        )

        # 'If' to avoid removing root folder, remove every other child folder
        if Path(root) != src_path:
            if result:
                result = True
            os.rmdir(root)

    return result


# Default behaviour
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "src_folder",
        help="Folder to sort through",
        metavar="<source_folder>",
        type=Path,
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        "-v",
        "--verbose",
        help="Print all changes made",
        action="store_true",
    )
    verbosity.add_argument(
        "-q",
        "--quiet",
        help="Do not print anything",
        action="store_true",
    )

    folder_name_separating = parser.add_mutually_exclusive_group()
    folder_name_separating.add_argument(
        "-s",
        "--separator",
        help="Custom folder name to file separator",
        type=str,
        nargs="?",
        default="-",
    )
    folder_name_separating.add_argument(
        "--no-folder-name",
        help="Do not prepend the folder name to moved files [Potential conflicting file names overwriting!]",
        action="store_false",
        dest="folder_name",
    )

    args = parser.parse_args()

    src_folder = Path(path.abspath(args.src_folder))

    were_folders_deleted = remove_child_folders(
        src_folder,
        args.verbose,
        args.separator,
        folder_name=args.folder_name,
    )

    print(
        "Done", "\nFolders were deleted" if were_folders_deleted else ""
    ) if not args.silent else ""
