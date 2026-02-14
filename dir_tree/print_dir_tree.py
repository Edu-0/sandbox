import os
from typing import List

def spacing(identation):
    space = "    " * identation
    return space

def extension_sorting(dir_list: List[str], path) -> List[str]:
    dir_list = sorted(dir_list, key=str.lower)

    folders = [file for file in dir_list if os.path.isdir(os.path.join(path, file))]
    files = [file for file in dir_list if not os.path.isdir(os.path.join(path, file))]

    return folders + files

def print_path_onwards(path, identation):

    try:
        dir_list = os.listdir(path)
        ordered_dir = extension_sorting(dir_list, path)
    except NotADirectoryError:
        print(spacing(identation), os.path.split(path)[1])
        return
    except PermissionError:
        print(spacing(identation), os.path.split(path)[1])
        return

    for item in ordered_dir:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            print(spacing(identation), os.path.join(path, item))
            print_path_onwards(item_path, identation + 1)
        else:
            print(spacing(identation), item)

#absolute_path = os.path.join("C:", "\Program Files (x86)", "Steam", "steamapps", "common") # Example

absolute_path = input("Enter absolute path: ")

print_path_onwards(absolute_path, 0)