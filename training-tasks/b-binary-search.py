import math


def binary_search(nums: list, tar, lb=-1, rb=-1) -> int:
    if len(nums) == 0:
        return -1
    lb, rb = 0 if lb == -1 else lb, len(nums) - 1 if rb == -1 else rb
    if rb - lb < 2:
        if nums[lb] == tar:
            return lb
        return rb if nums[rb] == tar else -1
    mid = lb + math.ceil((rb - lb) / 2)
    left = True if nums[mid] >= tar else False
    return binary_search(nums, tar, lb=lb if left else mid, rb=rb if not left else mid)


if __name__ == '__main__':
    arr = list(map(int, input().split()))
    while True:
        try:
            search = int(input().split()[1])
        except EOFError:
            break
        print(binary_search(arr, search))
