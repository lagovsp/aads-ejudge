def qpow(a, x: int):
    if x < 0:
        return 1 / qpow(a, -x)
    if x == 0:
        return 1
    if x == 1:
        return a
    if x == 2:
        return a * a
    hp = qpow(a, int(x / 2))
    return a * hp * hp if x % 2 != 0 else hp * hp


if __name__ == '__main__':
    base, power = int(input()), int(input())
    print(f'{base} to the power of {power}')
    print(f'We say {qpow(base, power)}')
    print(f'Python {base ** power}')
