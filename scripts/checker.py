# Copyright Sergey Lagov 2022

from sys import argv
from colorama import init, Fore
import os


# argv[1] — correct answer path
# argv[2] — user output path
# argv[3] (optional) — check mode: no — no-order (order of lines does not matter)


def parse_new_lines(lines: list) -> list:
    if not lines:
        return lines
    if lines[-1] and lines[-1][-1] == '\n':
        lines.append('')
    return list(map(lambda x: x.rstrip('\n'), lines))


def check_order(user_in: list, correct_in: list) -> bool:
    for i, correct in enumerate(correct_in):
        if not correct == user_in[i]:
            print(Fore.RED + f'ERROR line {i + 1}')
            print(Fore.RESET + f'\t\t\t       Correct: "{correct}"')
            print(Fore.RED + f'\t\t\t       Wrong: "{user_in[i]}"')
            return False
    return True


def check_no_order(user_in: list, correct_in: list) -> bool:
    corrects = dict()
    for line in correct_in:
        if line in corrects:
            corrects[line] += 1
            continue
        corrects.update({line: 1})

    unique_counter = 0
    for i, answer_line in enumerate(user_in):
        if answer_line in corrects:
            corrects[answer_line] -= 1
            unique_counter += 1 if corrects[answer_line] == 0 else 0

    if unique_counter == len(corrects) and len(user_in) == len(correct_in):
        return True

    for correct, times in corrects.items():
        if not times == 0:
            print(f'\t\t\t       Need {times}    "' + Fore.GREEN + f'{correct}' + Fore.RESET + '"')

    users_dict = dict()
    for ui in user_in:
        if ui in users_dict:
            users_dict[ui] += 1
            continue
        users_dict.update({ui: 1})

    for correct in corrects:
        if correct in users_dict:
            users_dict[correct] -= 1
    for entry, times in users_dict.items():
        if not times == 0:
            print(f'\t\t\t       Excess {times}  "' + Fore.RED + f'{entry}' + Fore.RESET + '"')
    return False


def main():
    init(autoreset=True)
    if len(argv) not in [3, 4]:
        return

    order_matters = True
    if len(argv) == 4 and argv[3] == 'no':
        order_matters = False

    for i in range(1, 3):
        if not os.path.exists(argv[1]):
            print(f'File {argv[1]} not found')
            return

    with open(argv[1]) as f1:
        with open(argv[2]) as f2:
            corrects = parse_new_lines(f1.readlines())
            users = parse_new_lines(f2.readlines())

    if not len(corrects) == len(users):
        print(Fore.RED + f'Numbers of lines differ ' +
              Fore.WHITE + f'{len(corrects)} != ' +
              Fore.RED + f'{len(users)}')

    status = check_order(users, corrects) if order_matters else check_no_order(users, corrects)
    if status:
        print(Fore.GREEN + 'PASS')


if __name__ == '__main__':
    main()
