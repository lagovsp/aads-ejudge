# Copyright Sergey Lagov 2022 lagovsp@gmail.com

def find_most_common():
    line = input()
    nums = line.split(' ')
    vals_to_times = {}
    for num in nums:
        if num in vals_to_times:
            vals_to_times[num] += 1
        else:
            vals_to_times[num] = 1
    max_entries = max(vals_to_times.items(), key=lambda x: x[1])[1]
    winners = []
    for el in vals_to_times.items():
        if el[1] == max_entries:
            winners.append(el[0])
    return min(winners)


if __name__ == '__main__':
    print(find_most_common())
