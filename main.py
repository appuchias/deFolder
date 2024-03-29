import os, argparse, stat
from pathlib import Path
from typing import get_args


# Checks if there is a folder inside the specified path
def is_there_a_folder(src_path: str) -> bool:
    assert os.path.exists(src_path), "Provided path does not exist."

    # If there is a folder, return True
    return not all([file.is_file() for file in os.scandir(src_path)])


# Check if text needs to be printed and print it in that case
def output(text: str, is_verbose: bool):
    """Output text to the console if condition is met (is_verbose in this case)"""
    if is_verbose:
        print(text)


# Removes folders recursively moving files upwards in the directory tree. Returns False if no folders were deleted
def defolder(
    src_path: Path,
    is_verbose: bool = True,
    separator: str = "-",
    folder_name: bool = True,
):
    if not separator:
        separator = "-"

    src_path = Path(str(src_path).strip("/").strip("\\"))

    assert os.path.exists(src_path), "Provided path does not exist."

    output("Running deFolder in " + str(src_path), is_verbose)

    # While added to repeat the loop in consecutive folders
    while is_there_a_folder(src_path):

        # Cycle through all the files in each folder
        for root, _, files in os.walk(src_path):

            # Avoid moving files in the root folder
            if Path(root) != src_path:
                for element in files:
                    # Get the file path as a path object
                    file_path = Path(os.path.join(root, element))

                    # Create the string containing the folder and separator
                    if folder_name:
                        folder_and_separator = str(file_path.parent) + separator.strip()
                    else:
                        folder_and_separator = ""

                    # Move the file itself
                    os.rename(
                        file_path,
                        os.path.join(
                            src_path,
                            folder_and_separator + element,
                        ),
                    )

                    output(
                        "mv:"
                        + str(file_path)
                        + "->"
                        + os.path.join(src_path, folder_and_separator + element),
                        is_verbose,
                    )

        # 'If' to avoid removing root folder, remove every other child folder
        if Path(root) != src_path:
            output("rm: " + root, is_verbose)  # Display removed folders

            try:
                os.rmdir(root)
            except PermissionError:
                # Give permissions to file
                os.chmod(root, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                os.rmdir(root)


# Get argparse args
def get_args() -> argparse.Namespace:
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

    defolder(
        src_folder,
        args.verbose,
        args.separator,
        folder_name=args.folder_name,
    )

    print("Finished.") if not args.quiet else ""
