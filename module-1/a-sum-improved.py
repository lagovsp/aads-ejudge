# Copyright Sergey Lagov 2022 lagovsp@gmail.com

from string import digits
import sys


def get_sum() -> int:  # w/o excess data structures
    s = 0
    minus, prev_digit = False, False
    for line in sys.stdin:
        current = 0
        for c in line:
            if c in digits:
                if prev_digit:
                    current = current * 10 + (-int(c) if minus else int(c))
                else:
                    current = -int(c) if minus else int(c)
                prev_digit = True
            else:
                s += current
                current = 0
                minus, prev_digit = True if c == '-' else False, False
        s += current
    return s


if __name__ == '__main__':
    print(get_sum())
