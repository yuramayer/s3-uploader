"""Additional funcs for the script"""

from pathlib import Path


def get_file_path() -> str:
    """Gets path to the file from user"""

    path_input = input('Type the path to the file: ')
    path = Path(path_input).expanduser()
    return path


def normalize_path(file_path: Path) -> Path:
    """Checks if the file in the file path"""

    # let's start with the absolute one
    if file_path.is_absolute() and file_path.exists():
        return file_path.resolve(strict=True)

    # then we're checking relative path
    rel_path = Path.cwd() / file_path

    if rel_path.exists():
        return rel_path.resolve(strict=True)

    raise FileNotFoundError(f"Couldn't find the: {file_path}")


def get_file_key(file_path: Path, parent_dir=None) -> str:
    """Creates key for the file. RN it's file name, mb changes later"""
    if parent_dir:
        rel_path = parent_dir.name / file_path.relative_to(parent_dir)
    else:
        base_path = file_path.parent
        rel_path = file_path.relative_to(base_path)

    return rel_path.as_posix()
