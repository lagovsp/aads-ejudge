def find_most_common():
    line = input()
    nums = line.split(' ')
    vals_to_times = {}
    for num in nums:
        if num in vals_to_times:
            vals_to_times[num] += 1
        else:
            vals_to_times[num] = 1
    pairs = sorted(vals_to_times.items(), key=lambda x: x[1], reverse=True)
    winners = []
    max_entries = pairs[0][1]
    for pair in pairs:
        if pair[1] == max_entries:
            winners.append(pair[0])
        else:
            break
    return min(winners)


if __name__ == '__main__':
    print(find_most_common())
