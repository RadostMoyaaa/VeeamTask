import argparse
import xml.etree.ElementTree as ET
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, help="Type directory to config file", default='config.xml')
args = parser.parse_args()


class RootTagException(Exception):  # Пользовательская ошибка корневого тега
    pass


def get_xml_tree(file_name):  # Функция получения xml дерева
    xml_tree = ET.parse(file_name)
    return xml_tree


def get_valid_elements_from_root(xml_tree, root_tag, child_tag, to_find):   # Функция получения валидных элементов из корня
    valid_list = []
    root = xml_tree.getroot()
    if root.tag != root_tag:
        raise RootTagException(f'Error: xml_tree root tag - {root.tag}, expected - {root_tag}')
    for file in root.findall(child_tag):
        valid = True
        for name in to_find:
            if name not in file.attrib or file.attrib[name] == '':
                valid = False
        if valid:
            print(f'Find valid: {file.attrib}')
            valid_list.append(file.attrib)
        else:
            print(f'Find not_valid: {file.attrib}')
    print('\n')
    return valid_list


def check_paths(source_path, destination_path, file_name, paths):  # Функция проверки путей
    for path in paths:
        source = os.path.join(path[source_path], path[file_name])
        destination = path[destination_path]
        file = path[file_name]
        if os.path.exists(source):
            copy_files(source=source, destination=destination, file=file)
        else:
            print(f"Source {source} or file {file} doesn't exist, going next")
            continue
        print('\n')


def copy_files(source, destination, file):  # Функция проверки пути копирования
    print(f"Source {source} is exist")
    destination_with_file = os.path.join(destination, file)
    if not os.path.exists(destination):
        print(f"Destination {destination} doesn't exist, creating...")
        try:
            os.mkdir(destination)
        except OSError as e:
            print(f"{e} - can't create directory {destination}, going next ")
            return
    do_copy(destination_with_file, source)


def do_copy(destination_with_file, source):  # Функция копирования
    try:
        shutil.copy(source, destination_with_file)
        print(f"File {destination_with_file} is copied")
    except PermissionError as e:
        print(f"{e} - PermissionError when coping")


if __name__ == '__main__':
    to_find = ['source_path', 'destination_path', 'file_name']
    ROOT_TAG = 'config'
    CHILD_TAG = 'file'
    try:
        xml_tree = get_xml_tree(args.config)
    except FileNotFoundError as e:
        print(e)
    else:
        try:
            valid_list = get_valid_elements_from_root(xml_tree, root_tag=ROOT_TAG, child_tag=CHILD_TAG, to_find=to_find)
        except RootTagException as e:
            print(e)
        else:
            check_paths(*to_find, paths=valid_list)
