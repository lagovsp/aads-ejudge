import sys


def read_and_write_sum():
    sum = 0
    with open(sys.argv[1], 'r') as f:
        for line in f:
            sum += 0 if line == '\n' else int(line)
    with open(sys.argv[2], 'w') as f:
        f.write(str(sum % 256))


if __name__ == '__main__':
    read_and_write_sum()
