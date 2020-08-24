from pathlib import Path


def does_file_exist(file_path):
    file = Path(file_path)
    return file.is_file()


def mkdir(name):
    Path(name).mkdir(parents=True, exist_ok=True)


def touch(name):
    Path(name).touch(exist_ok=True)
