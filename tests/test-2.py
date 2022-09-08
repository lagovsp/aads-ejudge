from string import digits
import sys


def get_sum() -> int:
    nums = []
    minus, prev_digit = False, False
    for line in sys.stdin:
        for c in line:
            if c in digits:
                if prev_digit:
                    nums[-1] = nums[-1] * 10 + (-int(c) if minus else int(c))
                else:
                    nums.append(-int(c) if minus else int(c))
                prev_digit = True
            else:
                minus, prev_digit = True if c == '-' else False, False
    return sum(nums)


if __name__ == '__main__':
    print(get_sum())
