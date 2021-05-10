import os
import hashlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, help="Type directory to input file", required=True)
parser.add_argument("--files_check", type=str, help="Type directory to files to check", required=True)
args = parser.parse_args()


def parse_input(file_path):  # Функция считывания файла с информацией о файлах для проверки
    with open(file_path, 'r') as f:
        res = f.readlines()
    return res


def check_file_hash(file, hash_obj, hash_sum):  # Функция проверки хэшэй файлов
    while True:
        data = file.read(CHUNK_SIZE)
        hash_obj.update(data)
        if not data:
            break
    if hash_sum == hash_obj.hexdigest():
        return 'OK'
    else:
        return 'FAIL'


def open_files_to_check(check, directory):  # Функция открытия и проверки файлов
    for c in check:
        arguments = c.split()
        file_name = arguments[0]
        algorithm = arguments[1]
        hash_sum = arguments[2]
        try:
            with open(os.path.join(directory, file_name), 'rb') as f:
                if algorithm == 'md5':
                    status = check_file_hash(file=f, hash_obj=hashlib.md5(), hash_sum=hash_sum)
                elif algorithm == 'sha1':
                    status = check_file_hash(file=f, hash_obj=hashlib.sha1(), hash_sum=hash_sum)
                elif algorithm == 'sha256':
                    status = check_file_hash(file=f, hash_obj=hashlib.sha256(), hash_sum=hash_sum)
                else:
                    print(f'Unexpected algorithm {algorithm}, file {f.name}')
                    continue
        except FileNotFoundError:
            status = 'Not found'
        print(file_name, status)


if __name__ == '__main__':
    CHUNK_SIZE = 2048
    try:
        lines = parse_input(args.input)
    except FileNotFoundError as e:
        print(e)
    else:
        open_files_to_check(lines, args.files_check)
