"""Base module, script is starting here"""

from utils import get_file_path, normalize_path, get_file_key
from uploader import upload_file_s3


def main():
    """Main script func"""

    path_str = get_file_path()
    local_path = normalize_path(path_str)

    if local_path.is_file():
        key = get_file_key(local_path)
        upload_file_s3(local_path, key)

    elif local_path.is_dir():

        for file in local_path.rglob('*'):
            if file.is_file():
                key = get_file_key(file, parent_dir=local_path)
                upload_file_s3(file, key)


if __name__ == '__main__':
    main()
