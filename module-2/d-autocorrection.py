# Copyright Sergey Lagov 2022 lagovsp@gmail.com

from enum import Enum
import math


class Trie:
    class ResultType(Enum):
        MATCHED = 0
        SUGGESTED = 1
        UNKNOWN = 2

    class Node:
        def __init__(self, li=None, pl=None, p=None, t=None):
            self.list_index = li  # Какой индекс у слова в списке слов дерева, префиксом которого это слово является
            self.pref_len = pl  # Префиксом какой длины слово этой вершины является для листа
            self.parent = p
            self.children = dict()  # Ключи - первые символы следующих переходов, значения - вершины
            self.is_terminal = t  # Заканчивается ли здесь слово

        def split(self, split_len: int, words: list) -> 'Node':
            if not 0 < split_len < self.parent.pref_len - self.pref_len:
                raise Exception('split length error')
            nn = Trie.Node(li=self.list_index, pl=split_len, p=self.parent, t=False)
            self.parent.children[words[self.list_index][self.parent.pref_len + 1]] = nn
            self.parent = nn
            nn.children[words[self.list_index][nn.pref_len + 1]] = self
            return nn

    @staticmethod
    def damerau_levenshtein_dist(w1: str, w2: str) -> int:
        '''
        Алгоритм поиска расстояния Дамерау-Левенштейна между двумя строками.
        Заполняем таблицу, как продемонстрировано в конспекте (с. 142)

        Временная сложность в худшем случае - O(|a|*|b|),
        так как в матрице |a|*|b| клеток

        Временная сложность в лучшем случае (хотя бы одна из строк пустая) - O(1)

        Пространственная сложность - O(min(|a|,|b|)).
        Выбираем наименьшее из слов, располагаем его горизонтально,
        чтобы длина строки была минимальна.
        Для подсчёта клетки необходимы лишь 3 последние строки - храним только их
        '''

        if not w1 or not w2:
            return max(len(w1), len(w2))
        if len(w2) < len(w1):
            w1, w2 = w2, w1
        lines = [  # prev_prev, prev, and last
            [i for i in range(len(w1) + 1)],
            [None] * (len(w1) + 1),
            [None] * (len(w1) + 1),
        ]
        cur_line = 1
        while not cur_line > len(w2):
            i, pi, ppi = cur_line % 3, (cur_line - 1) % 3, (cur_line - 2) % 3
            lines[i][0] = cur_line
            for j in range(1, len(w1) + 1):
                s = 0 if w1[j - 1] == w2[cur_line - 1] else 1
                transposition = math.inf
                if cur_line > 1 and j > 1:
                    t = 1 if w1[j - 1] == w2[cur_line - 2] and w1[j - 2] == w2[cur_line - 1] else math.inf
                    transposition = lines[ppi][j - 2] + t
                lines[i][j] = min(
                    lines[i][j - 1] + 1,
                    lines[pi][j] + 1,
                    lines[pi][j - 1] + s,
                    transposition,
                )
            cur_line += 1
        return lines[(cur_line - 1) % 3][-1]

    def __init__(self):
        self.root = Trie.Node()
        # Здесь хранятся терминальные строки.
        # Вершины содержат ссылки на слова из списка и длины префикса, которым эти вершины соответствуют
        # Строки в Python очень тяжелые. Если бы мы хранили строки в вершинах, было бы n строк.
        # При таком подходе количество строк равно количеству листьев, два int должны весить меньше
        self.words = list()

    def add_word(self, word: str):
        cur_index, cur_node = 0, self.root
        while True:
            child = cur_node.children.get(word[cur_index])
            if child is None:
                self.words.append(word)
                cur_node.children.update({word[cur_index]: Trie.Node(
                    len(self.words) - 1, len(word), p=cur_node, t=True)})
                return
            i = 0
            index = child.list_index
            # for i in range(child.parent.pref_len + 1, child.parent.pref_len + child.pref_len):
            #     if
            # while self.words[index]
            # if self.words[child.list_index][:child.pref_len]
            #     if len(child)
            #         cur_index += 1

    def check_word(self, word: str) -> (ResultType, list):
        return Trie.ResultType.MATCHED, []


def main():
    # w1 = 'список'
    # w2 = 'кипяток'

    w1 = 'вестибулярный'
    w2 = 'весна'

    print(Trie.damerau_levenshtein_dist(w1, w2))

    t, length = Trie(), int(input())

    for i in range(length):
        t.add_word(input())

    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            continue
        status, suggests = t.check_word(line)

        if status == Trie.ResultType.MATCHED:
            print(f'{line} - ok')
            continue
        if status == Trie.ResultType.SUGGESTED:
            print(f'{line} -> {", ".join(suggests)}')
            continue
        print(f'{line} -?')


if __name__ == '__main__':
    main()
