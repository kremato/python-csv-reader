
import sys

from typing import List


def get_last_section_index(line: str) -> int:

    comma: int = line.find(',')

    if comma == -1:
        return len(line)-1

    if not line.startswith('"'):
        return comma-1

    previous: str = line[0]
    for index, current in enumerate(line[1:]):
        if current == '"' and previous != '\\':
            comma = index+1
            break
        previous = current
    return comma


def parse_section(section: str) -> List[str]:

    if section.startswith('"') and section.endswith('"'):
        section = section[1:len(section)-1]

    section = section.replace('\\"', '"')

    return [section]


def parse(line: str) -> List[str]:
    line: str = line.replace('\n', '')
    result: List[str] = []
    while line:

        delimiter = get_last_section_index(line)

        # in both cases exclude comma, if there is one
        remainder = line[:delimiter+1]
        line = line[delimiter+2:]

        result += parse_section(remainder)

    return result


def read(path: str):
    parsed_result: List[List[str]] = []
    with open(path, 'r') as file:
        for line in file:
            parsed_result.append(parse(line))
    return parsed_result


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Wrong number of arguments. '
              'Program takes only one arg and that is the csv file path')
        exit()
    print(read(sys.argv[1]))
