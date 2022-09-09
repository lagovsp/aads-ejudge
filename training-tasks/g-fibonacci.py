from copy import deepcopy


def main(num):
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
