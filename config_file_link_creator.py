# B"H

# config-file-link-creator

from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List, Optional
import os
import filecmp

class Settings(BaseSettings):
    HOME_DIR: str
    BACKUP_DIR: str
    IGNORE: str

    class Config:
        env_file = '.env'

settings = Settings()

if not settings.HOME_DIR.is_dir():
    raise Exception(f'HOME_DIR does not exist:\n{settings.HOME_DIR}')

elif not settings.BACKUP_DIR.is_dir():
    raise Exception(f'BACKUP_DIR does not exist:\n{settings.BACKUP_DIR}')

elif not settings.IGNORE.is_file():
    raise Exception(f'IGNORE does not exist:\n{settings.IGNORE}')

# Check if directory was created
def check_dir(
    dir: Path
):

  if dir.is_dir():
      print(f'Directory: {dir} created successfully')

  else:
      raise Exception(f'Directory: {dir} not created :)')

# Check if file was created
def check_file(filename):

    if filename.is_file():
        print(f'File: {filename} created successfully')

    else:
        raise Exception(f'File: {filename} not created :(')

# Bring contents of path_ignore_file into a list of Paths

with open(settings.IGNORE) as file:
    path_ignore_list = [Path(line.rstrip()) for line in file]

# Check the path and create the link or directory as appropriate

def create_path(
    source_path: Path,
    destination_path: Path,
    path_ignore_list: List[Path]
) -> bool:

    if source_path not in path_ignore_list:

        if source_path.is_dir():

            if not destination_path.is_dir():

                destination_path.mkdir()
                check_dir(destination_path)

            return True

        elif destination_path.is_file():

            if filecmp.cmp(source_path, destination_path, shallow=False):

                destination_path.unlink()
                os.link(source_path, destination_path)
                check_file(destination_path)

                return False

            else:

                overwrite = input(f"{destination_path} exists with different contents from {source_path}. Overwrite?")

                if overwrite in ["y", "Y"]:

                     destination_path.unlink()
                     os.link(source_path, destination_path)
                     check_file(destination_path)

                return False

        else:

            os.link(source_path, destination_path)
            check_file(destination_path)

    else:
        print(f"{source_path} is in 'ignore' list")
        return False

# Create all the paths recursively
def create_all_paths(
    source_path: Path,
    destination_path: Path,
    path_ignore_list: Path
) -> None:

    for path in sorted(source_path.glob('*')):

        working_path = (destination_path / path.relative_to(settings.BACKUP_DIR))

        if create_path(path, working_path, path_ignore_list):
            create_all_paths(path, destination_path, path_ignore_list)

create_all_paths(Path(settings.BACKUP_DIR), Path(settings.HOME_DIR), path_ignore_list)