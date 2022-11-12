# Copyright Sergey Lagov 2022

from sys import argv
from colorama import init, Fore
import os


# argv[1] - correct answer
# argv[2] - user output

def parse_new_lines(lines: list) -> list:
    if not lines:
        return lines
    if lines[-1] and lines[-1][-1] == '\n':
        lines.append('')
    return list(map(lambda x: x.rstrip('\n'), lines))


def main():
    init(autoreset=True)
    if len(argv) != 3:
        return

    for i in range(1, 3):
        if not os.path.exists(argv[1]):
            print(f'File {argv[1]} not found')
            return

    with open(argv[1]) as f1:
        with open(argv[2]) as f2:
            corrects = parse_new_lines(f1.readlines())
            users = parse_new_lines(f2.readlines())

    if not len(corrects) == len(users):
        print(Fore.RED + f'ERROR (numbers of lines differ) ' +
              Fore.WHITE + f'{len(corrects)} != ' +
              Fore.RED + f'{len(users)}')
        return

    for i, correct in enumerate(corrects):
        if not correct == users[i]:
            print(Fore.RED + f'ERROR line {i + 1} ' +
                  Fore.WHITE + f'Correct: "{correct}"' +
                  Fore.RED + f' Wrong: "{users[i]}"')
            return
    print(Fore.GREEN + 'PASS')


if __name__ == '__main__':
    main()
