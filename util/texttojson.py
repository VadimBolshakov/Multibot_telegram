"""Module create json file from text file."""
import json
import os
from logging import Logger


def convert_text_files_to_json(path: str, logger: Logger, encoding: str = 'utf-8') -> bool:
    """
    Convert all text files to json files in a given directory.

    :param path: Path to directory.
    :type path: str
    :param logger: project Logger for exception.
    :type logger: class Logger
    :param encoding: Encoding of file. Defaults to 'utf-8'.
    :type encoding: str, optional

    :raises json.JSONDecodeError: If json file is not valid.
    :raises FileNotFoundError: If file not found.
    :raises PermissionError: If permission denied.
    :raises OSError: If error with file.

    :return: True if success, False if not.
    :rtype: bool
    """

    try:
        for file in os.listdir(path):
            if file.endswith('.txt'):
                if not text_to_json(path + file, path + file.replace('.txt', '.json'), encoding=encoding):
                    raise json.JSONDecodeError('JSONDecodeError', path + file, 0)
        return True
    except json.JSONDecodeError as e:
        logger.exception(f'ConvertError: {str(e)}')
        return False
    except OSError as e:
        logger.exception(f'ConvertError: {str(e)}')
        return False


def found_file_in_dir(path: str, file_name: str) -> bool:
    """Found file in directory.

    :param path: Path to directory.
    :type path: str
    :param file_name: Name of file.
    :type file_name: str

    :return: True if file is found, False if not.
    :rtype: bool
    """
    for file in os.listdir(path):
        if file == file_name:
            return True
    return False


def text_to_json(file_source: str, file_target: str, encoding: str = 'utf-8',
                 indent: int = 4, ensure_ascii: bool = False) -> bool:
    """Convert text file to json file.

    Args:

        file_source (str): Path to source file.
        file_target (str): Path to target file.
        encoding (str, optional): Encoding of file. Defaults to 'utf-8'.
        indent (int, optional): Indent of json file. Defaults to 4.
        ensure_ascii (bool, optional): Ensure ascii. Defaults to False.

    Returns:
        True if success, False if not."""
    try:
        with open(file_source, 'r', encoding=encoding) as file:
            data = file.read()
            data_json = json.loads(data)

        with open(file_target, 'w', encoding='utf-8') as file:
            json.dump(data_json, file, ensure_ascii=ensure_ascii, indent=indent)

        return True
    except [FileNotFoundError, json.JSONDecodeError, Exception]:
        return False


if __name__ == '__main__':
    # path = './src/menu/'
    path_test = '../src/menu/'
    print(convert_text_files_to_json(path=path_test, logger=Logger('test')))
