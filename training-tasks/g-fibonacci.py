# Copyright Sergey Lagov 2022 lagovsp@gmail.com

from copy import deepcopy


def main(num):  # O(n) complexity provided, O(logn) is possible
    prelast = 0
    last = 1
    if num == 0 or num == 1:
        print(num)
        return
    for i in range(2, num + 1):
        buf = deepcopy(last)
        last = prelast + last
        prelast = buf
    print(last)


if __name__ == '__main__':
    main(int(input()))
