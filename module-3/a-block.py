# Copyright Sergey Lagov 2022 lagovsp@gmail.com

class Blocker:
    def __init__(self, n: int, p: int, b: int, b_max: int, cur: int):
        self.n = n
        self.p = p
        self.b_min = b
        self.b_max = b_max
        self.cur = cur
        self.tries = []

    def add_try(self, failure: int):
        if 2 * self.b_max >= self.cur - failure:
            self.tries.append(failure)

    def analyze(self) -> (bool, int):
        self.tries.sort()
        b_cur, blocked_before, block_start, try_num = self.b_min, False, 0, 0
        while try_num <= len(self.tries) - self.n:
            if self.tries[try_num + self.n - 1] - self.tries[try_num] >= self.p:
                try_num += 1
                continue
            if blocked_before:
                b_cur *= 2
                b_cur = self.b_max if b_cur > self.b_max else b_cur
            try_num += self.n
            block_start, blocked_before = self.tries[try_num - 1], True
        if block_start + b_cur < self.cur or not blocked_before:
            return False, None
        return True, block_start + b_cur


def main():
    """
    В условии задачи ничего не сказано о инкапсуляции — за её соблюдением я не следил

    Сперва мы записываем наши n попыток в массив — O(n)
    Затем сортируем массив размера n по возрастанию — O(n*logn)
    Далее совершаем проход по массиву для выяснения статуса блокировки — O(n)
    => Время работы алгоритма — O(n + n*logn + n) = O(n*logn)

    Согласно документации, sort в Python — Timsort. Сложность Timsort по памяти — O(n)
    Хранение массива с попытками обойдётся в O(n)
    => Сложность алгоритма по памяти — O(n)
    """
    try:
        n, p, b, b_max, cur_unix = map(int, input().split())
    except Exception:
        return

    blocker = Blocker(n, p, b, b_max, cur_unix)
    while True:
        try:
            blocker.add_try(int(input()))
        except EOFError:
            break

    status, time = blocker.analyze()
    print(time if status else 'ok')


if __name__ == '__main__':
    main()
