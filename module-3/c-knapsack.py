# Copyright Sergey Lagov 2022 lagovsp@gmail.com

class Item:
    def __init__(self, weight: int, cost: int):
        self.weight = weight
        self.cost = cost
        self.cost_scaled = cost


class KnapsackSet:
    """
    Объект-решение, возвращаемый алгоритмом в качестве ответа.
    Поля как будто не подогнаны под формат вывода.
    Иметь в одном месте общий вес и стоимость, а также индексы
    добавленных в оптимальную конфигурацию рюкзака объектов кажется логичным
    """

    def __init__(self, ids=None, w=None, c=None):
        self.items_ids = ids if ids is not None else list()
        self.total_weight = w if w is not None else 0
        self.total_cost = c if c is not None else 0


class KnapsackFPTAS:
    def __init__(self, e: float, capacity: int):
        self.e = e
        self.capacity = capacity
        self.items = dict()
        self.max_cost = 0
        self.scale = 1
        self.added = 0

    def __round_cost(self, cost: int) -> int:
        return int(cost / self.scale)

    def add_item(self, w: int, c: int):
        """
        Алгоритм должен быть инкапсулирован.
        Пользователь изначально не знает, какие вещи явно можно отбросить из-за того,
        что они не помещаются в рюкзак, поэтому делаем вид, что добавляем все.
        Естественно, добавлять/рассматривать вещи, вес которых больше вместимости
        рюкзака мы никогда не станем — просто увеличиваем счетчик, сохраняя порядок
        и корректность будущего ответа по отношению к пользователю
        """
        if w <= self.capacity:
            self.items.update({self.added: Item(w, c)})
            self.max_cost = c if c > self.max_cost else self.max_cost
        self.added += 1

    def solve(self) -> KnapsackSet:
        if not self.items:
            return KnapsackSet()

        self.scale = self.e * self.max_cost / (len(self.items) * (1 + self.e))
        for item in self.items.values():
            item.cost_scaled = self.__round_cost(item.cost)
        sols = {0: KnapsackSet()}

        for id, item in self.items.items():
            sols_snapshot = list(sols.values())
            for sol in sols_snapshot:
                new_weight, new_cost = sol.total_weight + item.weight, sol.total_cost + item.cost_scaled
                if new_weight > self.capacity:
                    continue
                if new_cost not in sols or new_weight < sols[new_cost].total_weight:
                    sols[new_cost] = KnapsackSet(sol.items_ids + [id], new_weight, new_cost)

        best = sols.get(max(sols.keys()))
        best.total_cost = 0
        for id in best.items_ids:
            best.total_cost += self.items[id].cost
        return best


def main():
    """
    Логично, что алгоритм возвращает номера объектов, присутствующих в оптимальной
    сборке рюкзака, опираясь на порядок их добавления. Номера объектам алгоритм
    присваивает сам — ввод индекса от пользователя никак не подразумевается
    (он ведь может случайно ввести один индекс дважды и все поломается)
    """
    try:
        knapsack = KnapsackFPTAS(float(input()), int(input()))
    except EOFError:
        return

    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            continue
        knapsack.add_item(*map(int, line.split()))

    solution = knapsack.solve()
    print(solution.total_weight, solution.total_cost)
    for id in solution.items_ids:
        print(id + 1)


if __name__ == '__main__':
    main()
