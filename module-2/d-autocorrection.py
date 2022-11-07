# Copyright Sergey Lagov 2022 lagovsp@gmail.com

from enum import Enum


class Trie:
    class ResultType(Enum):
        MATCHED = 0
        SUGGESTED = 1
        UNKNOWN = 2

    class Node:
        def __init__(self, s=None, t=None):
            self.substr = s
            self.is_terminal = t  # Заканчивается ли здесь слово
            self.children = dict()  # Ключи - первые символы следующих переходов, значения - вершины
            # print(f'Trie.Node created {self}')
            # print(f'    self.substr = "{self.substr}"')
            # print(f'    self.is_terminal = "{self.is_terminal}"')
            # print(f'    self.children = "{self.children}"')

    def __init__(self):
        self.root = Trie.Node(s='', t=False)

    @staticmethod
    def __split(p: 'Trie.Node', child: 'Trie.Node', cpl: int, word: str):
        med = Trie.Node(s=child.substr[:cpl], t=False)
        child.substr = child.substr[cpl:]
        child.parent = med
        new = Trie.Node(s=word, t=True)
        med.children = {child.substr[0]: child, word[0]: new}
        p.children.update({med.substr[0]: med})

    @staticmethod
    def __mark_terminal(p: 'Trie.Node', child: 'Trie.Node', i: int):
        new = Trie.Node(s=child.substr[:i], p=p, t=True)
        new.children.update({child.substr[i + 1]: child})
        p.children[child.substr[0]] = new
        child.parent = new

    def add_word(self, word: str):
        '''
        Алгоритм добавления слова в сжатое префиксное дерево (далее - словарь).
        Совершаем переходы только по нужным нам буквам, параллельно сверяя текущий путь с добавляемым словом word.

        Временная сложность алгоритма - O(k), где k - длина добавляемого слова word.
        Пространственная сложность алгоритма - O(1).
        '''

        pass

    def find_word(self, word: str) -> bool:
        '''
        Алгоритм поиска слова (word) в словарь.

        Переходим только в вершины, первая буква перехода (добавляемой подстроки) которых соответствует следующей букве
        искомого слова. Остальные вершины проверять нет смысла. Если слово закончилось и мы находимся в терминальной
        вершине (на ней заканчивается слово в словаре), то возвращаем True. Иначе - False.

        Временная сложность алгоритма - O(k), где k - длина запроса (слово word).
        Пространственная сложность алгоритма - O(1).
        '''

        if not word and self.root.is_terminal:
            return True
        cur_node, cur_str, word_i, cur_str_i = self.root, self.root.substr, 0, 0
        while word_i < len(word) and cur_node is not None:
            if word[word_i] != cur_str[cur_str_i]:
                return False
            if cur_str_i != len(cur_str) - 1:
                continue
            if word_i == len(word) - 1 and cur_node.is_terminal:
                return True
            if not word_i + 1 < len(word):
                return False
            cur_node, cur_str_i = cur_node.children.get(word[word_i + 1]), 0
            word_i += 1
        return False

    def suggest(self, word: str) -> (ResultType, list):
        '''
        Алгоритм поиска слов в словаре, чьи расстояния Дамерау-Левенштейна (далее - Д-Л) до запроса word не больше 1.
        Рекурсивный алгоритм обходит словарь в глубину, накапливая расстояние Д-Л, до момента, пока оно не больше 1.

        Временная сложность алгоритма - O(m * n^2), где m - мощность алфавита, а n - длина запроса.

        Докажем эту оценку.

        Рассмотрим худший случай. Сжатое префиксное дерево выродилось в полное m-арное префиксное дерево,
        в каждой вершине которого находится лишь 1 символ.

        Пусть слово word при проверке дойдет до листа (и будет отстоять по Д-Л на 1 от находящегося в словаре
        корректного слова, т.е. ошибка в слове word, например, - лишний символ на конце).

        Пусть i - счетчик пройденных ярусов дерева. Идем от корня, i = 0.

        При каждом переходе на следующий ярус мы должны будем проверить как путь, содержащий в себе слово word,
        так и остальные m-1 вершин, так как счетчик ошибок равен нулю (при переходе в каждую из m-1 вершин счетчик
        увеличивается на 1).

        Так как мы рассматриваем случай, где поиск дойдет до листов дерева, а длина запроса - n, то высота дерева,
        которая ранее определялась как log<m>(|V|) (логарифм по основанию m от мощности мн-ва V), где V - мн-во
        вершин дерева, теперь будет определяться как n => h = n.

        Типы ошибок по Д-Л: вставка (В), замена (З), удаление (У), транспозиция (Т).

        В случае, если при переходе в какую-то из m-1 вершин мы увидели одну из ошибок (В), (З) или (У), то у текущего
        пути более нет права на ошибку => существует максимум 1 путь до листа, причем его длина будет h-i для i-ого
        яруса сверху.

        Если мы посчитали, что найдена ошибка (Т), то буква следующего перехода определена - та, которая поменяется
        местами с предыдущей (т.е. существует только 1 возможный вариант). Таким образом, для ошибки (Т) у нас также
        существует максимум 1 путь до листа, и его длина также равна h-i для i-ого яруса сверху.

        Запишем следующую сумму (все далее записанные суммы идут от i = 0 до n):

        ∑(1+(m-1)(n-i)) = n+∑(mn-n-im+i) = n+mn^2-n^2-m∑i+∑i = n^2(m-1)+n+(1-m)∑i = n^2(m-1)+n+(1-m)((0+n)/2*n) =
        = n^2(m-1)+n+(1-m)(n^2/2) = n^2(m-1)+n+n^2/2-mn^2/2 = n^2((m-1)+1/2-m/2)+n = n^2(m-1)/2+n = O(mn^2)

        Временная сложность алгоритма доказана.

        Пространственная сложность рекурсивного алгоритма - O(n), так как в стеке вызова может быть n кадров функции.
        '''

        pass


def main():
    # w1 = 'список'
    # w2 = 'кипяток'

    # w1 = 'вестибулярный'
    # w2 = 'весна'

    t, length = Trie(), int(input())

    i = 0
    while i < length:
        word = input()
        if not word:
            continue
        t.add_word(word)
        i += 1

    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            continue

        status, suggests = t.suggest(line)
        if status == Trie.ResultType.MATCHED:
            print(f'{line} - ok')
            continue
        if status == Trie.ResultType.SUGGESTED:
            print(f'{line} -> {", ".join(suggests)}')
            continue
        print(f'{line} -?')


if __name__ == '__main__':
    main()
