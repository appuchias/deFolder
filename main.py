import os, argparse, stat
from pathlib import Path
from typing import get_args


# Checks if there is a folder inside the specified path
def is_there_a_folder(src_path: str) -> bool:
    assert os.path.exists(src_path), "Provided path does not exist."

    # If there is a folder, break the loop and return True
    for element in os.scandir(src_path):
        if element.is_dir():
            break

    else:
        return False

    return True


# Removes folders recursively moving files upwards in the directory tree. Returns False if no folders were deleted
def defolder(
    src_path: Path,
    is_verbose: bool = True,
    separator: str = "-",
    folder_name: bool = True,
) -> bool:

    src_path = Path(str(src_path).strip("/").strip("\\"))

    assert os.path.exists(src_path), "Provided path does not exist."
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
                    file_path = Path(os.path.join(root, element))

                    # Move the file itself
                    folder_and_separator = (
                        (str(file_path.parent) + str(separator)) if folder_name else ""
                    )
                    os.rename(
                        file_path,
                        os.path.join(
                            src_path,
                            folder_and_separator + element,
                        ),
                    )

                    # UX
                    if is_verbose:
                        print(
                            "mv:",
                            file_path,
                            "->",
                            os.path.join(
                                src_path, str(file_path.parent) + "-" + element
                            ),
                        )

        # 'If' to avoid removing root folder, remove every other child folder
        if Path(root) != src_path:
            if result:
                result = True
            if is_verbose:  # Display removed folders
                print("rm:", root)

            try:
                os.rmdir(root)
            except PermissionError:
                # Give permissions to file
                os.chmod(root, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                os.rmdir(root)

    return result


# Get argparse args
def get_args():
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
        default="-",
    )
    folder_name_separating.add_argument(
        "--no-folder-name",
        help="Do not prepend the folder name to moved files [Potential conflicting file names overwriting!]",
        action="store_false",
        dest="folder_name",
    )

    return parser.parse_args()


# Default behavior
if __name__ == "__main__":
    args = get_args()

    src_folder = Path(os.path.abspath(args.src_folder))

    were_folders_deleted = defolder(
        src_folder,
        args.verbose,
        args.separator,
        folder_name=args.folder_name,
    )

    print(
        "Done", "\nFolders were deleted" if were_folders_deleted else "Failed"
    ) if not args.quiet else ""
