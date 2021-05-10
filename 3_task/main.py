import argparse
import time
import os
from abc import ABC, abstractmethod
import logging
import psutil
from os.path import expanduser

parser = argparse.ArgumentParser()
parser.add_argument("--log", type=str, help="Name of log file", default='info.log')
args = parser.parse_args()

LOG = logging.getLogger(__name__)  # Логер с именем испольняемого модуля
LOG.setLevel(logging.INFO)
LOG.propagate = False
LOG_FORMATTER = logging.Formatter(
    "%(asctime)s %(filename)s: %(levelname)s %(message)s")
FILE_LOGGING_HANDLER = logging.FileHandler(args.log, encoding="UTF-8")
FILE_LOGGING_HANDLER.setFormatter(LOG_FORMATTER)
LOG.addHandler(FILE_LOGGING_HANDLER)


class PrepareUnixTimeException(Exception):  # Пользовательская ошибка при нечетности времени
    pass


class PrepareMemoryException(Exception):  # Пользовательская ошибка при малом объеме памяти
    pass


class TestBase(ABC):  # Абстрактный базовый класс
    def __init__(self, tc_id: int, name: str):
        self.tc_id = tc_id
        self.name = name

    @abstractmethod
    def prepare(self):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError

    @abstractmethod
    def clean_up(self):
        raise NotImplementedError

    def execute(self):
        try:
            self.prepare()
            self.run()
            self.clean_up()
        except BaseException as e:
            LOG.info(f'TestCase {self.tc_id}, {self.name} is created, exception: {e}')


class TestCaseOne(TestBase):  # Наследник, первый тест кейс
    def __init__(self, tc_id: int, name: str):
        super().__init__(tc_id, name)
        LOG.info(f'TestCase {self.tc_id}, {self.name} is created')

    def prepare(self):
        t = int(time.time())
        LOG.info(f'TestCase: id - {self.tc_id}, name - {self.name} is checking time {t}')
        if t % 2 != 0:
            raise PrepareUnixTimeException(f'Prepare failed - {t} odd number!')

    def run(self):
        home_directory = expanduser("~")
        LOG.info(f'TestCase: id - {self.tc_id}, name - {self.name} is checking dir {home_directory}, files {os.listdir(path=home_directory)}')

    def clean_up(self):
        LOG.info(f'TestCase: id - {self.tc_id}, name - {self.name} is cleaning, nothing to clean')


class TestCaseTwo(TestBase):  # Наследник, второй тест кейс
    def __init__(self, tc_id: int, name: str):
        super().__init__(tc_id, name)
        self.random_file = None
        LOG.info(f'TestCase {self.tc_id}, {self.name} is created')

    def prepare(self):
        memory = psutil.virtual_memory()
        gb = int(memory.total / 1024 ** 3)
        LOG.info(f'TestCase: id - {self.tc_id}, name - {self.name} is checking memory {gb}Gb')
        if gb < 1:
            raise PrepareMemoryException(f'Prepare failed: PHYSICAL MEMORY {gb} < 1')

    def run(self, file_name='test', size=1024000):
        LOG.info(f'TestCase: id - {self.tc_id}, name - {self.name} is writing {size} bytes to file {file_name}')
        self.random_file = file_name
        with open(self.random_file, 'wb') as f:
            f.write(os.urandom(size))

    def clean_up(self):
        LOG.info(f'TestCase: id - {self.tc_id}, name - {self.name} is cleaning')
        os.remove(self.random_file)


if __name__ == '__main__':

    case_1 = TestCaseOne(tc_id=1, name='TestCase1')
    case_1.execute()

    case_2 = TestCaseTwo(tc_id=2, name='TestCase2')
    case_2.execute()
