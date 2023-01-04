import os
import sys
import re


def main():
    if len(sys.argv) != 2:
        return

    files = os.listdir(sys.argv[1])
    max_number = 0
    for file in files:
        if re.fullmatch(r'\d+\.dat', file):
            num = int(file[:-4])
            max_number = num if num > max_number else max_number
    print(max_number)
    sys.exit(max_number)


if __name__ == '__main__':
    main()
