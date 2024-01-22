# B"H

# config-file-link-creator

A script that makes links to all your config files from your repo into their proper places

It relies mainly on the `pathlib` library and partly on the `os` library.

Documentation for `pathlib` can be found at https://docs.python.org/3/library/pathlib.html

**Why hard links?**

https://www.geeksforgeeks.org/difference-between-hard-link-and-soft-link/

If the original files are deleted, hard links will remain functional.

## Setup

### A file for env variables should be created to look something like this

```
HOME_DIR = pathlib.Path('/home/baruch')
BACKUP_DIR = pathlib.Path('/home/baruch/repos/config/config_files')
IGNORE = backup_dir / '.path_ignore_file'
```

`HOME_DIR` is the path to your home directory where the links will be created.

`BACKUP_DIR` is the path to the directory in your backup repo where all the config files are backed up

`IGNORE` is the path to the file that contains a list of files and directories in your backup repo that you don't want linked

## The script itself

### Taking in the `.env` variables

First a class is made to bring in all the environment variables as path objects

### Testing functions

These are the functions that will check to see if the file or directory where created successfully later on. The will raise exceptions if something went wrong.

### Bringing in the paths from the `.path_ignore_file`

A class called `Paths` has one list of path objects. The list is populated by the `.path_ignore_file`

### Create approved paths

The function `create_path()` takes in three parameters. The first parameter is called `source_path`. It's the path to the file or directory in your repo that will be linked or created. The second parameter is called `destination_path`. It is the path in the home directory where the link or directory will be created. The third parameter is the `path_ignore_list`. `create_path()` returns a boolean value with indicates whether or not to proceed to create `destination_path`.

The boolean value it returns will indicate whether or not to recurse into the `source_path`.

The first thing `create_path()` does is it checks to see if `source_path` is in the `.path_ignore_list`. As long as the `source_path` is not in the `.path_ignore_list` it can proceed. Assuming it isn't, if the `source_path` is a directory, as long as there is no directory with the same in the `destination_path`, it creates the `destination_path` and returns `True`. Otherwise, it just returns, `True`.

Now `destination_path` needs to be checked. If `destination_path` is a file that already exist in the home file system, it checks to see if the contents are the same as the file `source_path`. If it is the same, it removes the file at `destination_path` and creates the link in its place. It returns `False`. If the contents are different, the user is asked whether on not to overwrite. In either case, it returns `False`. 

The last possibility is that `destination_path` is a file that does not exist yet. The link is created and `create_path()` returns `False`.

If `source_path` is in `.path_ignore_list`, `create_path()` simply returns false.

### Recursing through the backup directory

The function `create_all_paths()` binds everything together. It takes in three parameters: `source_path`, `destination_path`, and `path_ignore_list`. It first calls the variable `working_path`. That is the name of the file or directory as it will exist in the home directory. For example, if the `source_path` is `/backup/file`, then `working_path` will be `/home/file`. It iterates through the files and directories in `source_path` and runs `create_path()` on each of them. If `create_path()` returns `True`, it runs `create_all_paths()` using the current path in the loop.

### Last part

The variables `BACKUP_DIR`, `HOME_DIR`, and `path_ignore_list.paths` are passed into `create_all_paths()` which calls `create_path()` and, in the case of a directory, calls itself.