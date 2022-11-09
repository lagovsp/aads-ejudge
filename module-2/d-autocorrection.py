# Copyright Sergey Lagov 2022 lagovsp@gmail.com

class Trie:
    class Node:
        def __init__(self, s=None, t=None):
            self.substr = s
            self.is_terminal = t  # Заканчивается ли здесь слово
            self.children = dict()  # Ключи - первые символы следующих переходов, значения - вершины

        def add_child(self, substr: str):
            '''
            Добавляет к вершине вершину-ребёнка с переходом substr.

            Временная сложность - O(len(substr)+m), где m - мощность алфавита
            (m зависит от входных данных (добавляемых слов), а значит считать ее константой нельзя,
            хотя m и ограничена мощностью множества всех возможных символов.
            Пишем + m, так как в случае, если придется перестраивать хэш-таблицу (случается редко,
            особенно с двойным хэшированием, как в Python), её стоит учитывать).
            '''
            new = Trie.Node(s=substr, t=True)
            self.children.update({substr[0]: new})

        def extract(self, i: int, t=True):
            '''
            Отделяет последние k-i символов вершины в отдельную вершину
            (k - длина подстроки в данной вершине) и делает терминальный статус текущей как t.

            Временная сложность - O(k), где k - начальная длина подстроки (перехода) текущей вершины
            (точно делаем 2 слайса строки, покрывающие всю строку, добавление 1 элемента в пустую (!) хэш-таблицу - O(1)).
            '''
            if i == len(self.substr):
                self.is_terminal = t
                return
            new = Trie.Node(self.substr[i:], t=self.is_terminal)
            self.is_terminal = t
            self.substr = self.substr[:i]
            new.children = self.children
            self.children = {new.substr[0]: new}

        def split(self, i: int, substr: str):
            '''
            Разбивает вершину на две и подвешивает к верхней вершину-ребенка с переходом substr.

            Временная сложность O(k+len(substr)+m), где k - начальная длина подстроки (перехода) текущей вершины,
            (совокупность методов extract и add_child).
            '''
            self.extract(i, t=False)
            self.add_child(substr)

        def suggest(self, w: str, res: set, pi=None, mistake=False, acc=None):
            '''
            Алгоритм поиска слов в словаре, чьи расстояния Дамерау-Левенштейна (далее - Д-Л) до запроса word не больше 1.
            Рекурсивный алгоритм обходит словарь в глубину, накапливая расстояние Д-Л, до момента, пока оно не больше 1.

            Типы ошибок по Д-Л: вставка (В), замена (З), удаление (У), транспозиция (Т).

            Временная сложность алгоритма - O(m * n^2), где m - мощность алфавита, а n - длина запроса.

            Докажем эту оценку.

            1. Рассмотрим худший случай. Сжатое префиксное дерево выродилось в полное m-арное префиксное дерево,
            в каждой вершине которого находится лишь 1 символ.

            2. В худшем случае слово word при проверке дойдет до листа (и будет отстоять по Д-Л на 1 от находящегося в словаре
            корректного слова, т.е. ошибка в слове word, например, - лишний символ на конце).

            3. Пусть i - счетчик пройденных ярусов дерева. Спускаемся вниз, в корне i = 0.

            4. При каждом переходе на следующий ярус мы должны будем проверить как путь, содержащий в себе слово word,
            так и остальные m-1 вершин (по 4 раза каждую для каждой из возможных ошибок), так как счетчик ошибок для слова
            word остается равным 0 на протяжении всего обхода дерева (см. п. 2). Счетчик ошибок увеличивается на 1 при
            переходе в каждую из m-1 вершин на каждом ярусе.

            5. Так как мы рассматриваем случай, где поиск дойдет до листов дерева (см. п. 2), а длина запроса - n,
            то высота дерева h теперь будет определяться как O(n). h = O(n).

            6. В случае, если при переходе в какую-то из m-1 вершин мы проверяем одну из ошибок (В), (З) или (У), то
            текущий путь уже не сможет иметь ошибки в дальнейшем => на каждом ярусе для каждой из m-1 вершин существует
            максимум 1 допустимый путь до листа, причем его длина будет равна h-i, где i - номер текущего яруса (см. п. 3).

            7. В случае, если мы проверяем возможную ошибку (Т), то буква следующего перехода уже предопределена - та,
            которая поменяется местами с предыдущей (т.е. существует только 1 возможный вариант). Таким образом, для ошибки
            (Т) на каждом ярусе для каждой из m-1 вершины существует максимум 1 допустимый путь до листа. Его длина также
            равна h-i, где i - номер текущего яруса (см. п. 3).

            8. Тогда количество всех операций можно определить суммой (все далее записанные суммы от i = 0 до n):

            ∑(1+4(m-1)(h-i)) = ∑(1+4(m-1)(n-i)) = n+4∑(mn-n-im+i) = n+4mn^2-4n^2-4m∑i+4∑i = 4n^2(m-1)+n+4(1-m)∑i =
            = 4n^2(m-1)+n+4(1-m)((0+n)/2*n) = 4n^2(m-1)+n+2(1-m)(n^2) = n^2(4(m-1)-2(m-1))+n = 2n^2(m-1)+n = O(mn^2)

            Временная сложность алгоритма доказана.
            '''
            if acc is None:
                acc = ''
            if pi is None:
                pi = 0

            if mistake:
                if pi < len(w):
                    next_n = self.children.get(w[pi])
                    if next_n is None:
                        return
                    if not next_n.substr == w[pi:pi + len(next_n.substr)]:
                        return
                    if next_n.substr == w[pi:] and next_n.is_terminal:
                        res.add(acc + next_n.substr)
                    next_n.suggest(w, res, pi=pi + len(next_n.substr), mistake=True, acc=acc + next_n.substr)
                return

            def check_add(l):
                if l_new == l and node.is_terminal:
                    res.add(acc + node.substr)

            for node in self.children.values():
                ind, l_new = len(node.substr), len(acc + node.substr)
                for it, char in enumerate(node.substr):
                    if len(w) <= it + pi or not char == w[it + pi]:
                        ind = it
                        break

                if len(node.substr) == ind:
                    length = len(w)
                    if l_new in [length, length - 1] and node.is_terminal:
                        res.add(acc + node.substr)
                    node.suggest(w, res, pi=pi + ind, mistake=False, acc=acc + node.substr)
                    continue

                pi_ind = pi + ind
                pi_ind_1, pi_substr = pi_ind + 1, pi + len(node.substr)

                if node.substr[ind:] == w[pi_ind_1:l_new + 1]:
                    check_add(len(w) - 1)
                    node.suggest(w, res, pi=pi_substr + 1, mistake=True, acc=acc + node.substr)

                if node.substr[ind + 1:] == w[pi_ind:l_new - 1]:
                    check_add(len(w) + 1)
                    node.suggest(w, res, pi=pi_substr - 1, mistake=True, acc=acc + node.substr)

                if node.substr[ind + 1:] == w[pi_ind_1:l_new]:
                    check_add(len(w))
                    node.suggest(w, res, pi=pi_substr, mistake=True, acc=acc + node.substr)

                if pi_ind_1 < len(w) and w[pi_ind] in node.children and w[pi_ind_1] == node.substr[ind]:
                    adjusted = w[:pi_ind] + w[pi_ind_1] + w[pi_ind] + w[pi_ind_1 + 1:]
                    check_add(len(w))
                    node.suggest(adjusted, res, pi=pi_substr, mistake=True, acc=acc + node.substr)
                    continue

                if ind < len(node.substr) - 1 and pi_ind < len(w) - 1 and node.substr[ind] == w[pi_ind_1] and \
                        node.substr[ind + 1] == w[pi_ind] and node.substr[ind + 2:] == w[pi_ind_1 + 1:l_new]:
                    check_add(len(w))
                    node.suggest(w, res, pi=pi_substr, mistake=True, acc=acc + node.substr)

    def __init__(self):
        self.root = Trie.Node(s='', t=False)
        self.last_searched_for = None
        self.suggests = set()

    def add_word(self, word: str):
        '''
        Алгоритм добавления слова в сжатое префиксное дерево.
        Совершаем переходы только по нужным нам буквам, параллельно сверяя текущий путь с добавляемым словом word.

        Сложность алгоритма - O(n+len(w)+m), где
        n - длина добавляемого слова word,
        w - самое длинная подстрока (переход) во всём дереве,
        m - мощность алфавита.

        Идем по всему слову word (O(n)). В случае, если надо сделать extract или split,
        придется разбить какую-то вершину (O(len(w)+m)).
        '''
        if not word:
            return
        word = word.lower()
        cur_node, word_i, cur_str_i = self.root.children.get(word[0]), 0, 0
        if cur_node is None:
            self.root.add_child(word)
            return
        cur_str = cur_node.substr
        while True:
            if not word[word_i] == cur_str[cur_str_i]:
                cur_node.split(cur_str_i, word[word_i:])
                return
            word_i += 1
            cur_str_i += 1
            if cur_str_i == len(cur_str) and word_i < len(word):
                next_node, cur_str_i = cur_node.children.get(word[word_i]), 0
                if next_node is None:
                    cur_node.add_child(word[word_i:])
                    return
                cur_node = next_node
                cur_str = cur_node.substr
            if word_i == len(word) and cur_str_i < len(cur_str):
                cur_node.extract(cur_str_i)
                return
            if word_i == len(word) and word_i == len(word):
                cur_node.is_terminal = True
                return

    def find(self, word: str) -> bool:
        '''
        Алгоритм поиска слова (word) в словаре.

        Переходим только в вершины, первая буква перехода (добавляемой подстроки) которых соответствует следующей букве
        искомого слова. Остальные вершины проверять нет смысла. Если слово закончилось и мы находимся в терминальной
        вершине (на ней заканчивается слово в словаре), то возвращаем True. Иначе - False.

        Сложность алгоритма - O(n), где n - длина запроса (слово word).
        Идем по слову. Закончилось и мы на конце терминальной вершины - True. Иначе - False.
        '''
        if not word:
            return False
        word = word.lower()
        cur_node, word_i, cur_str_i = self.root.children.get(word[0]), 0, 0
        if cur_node is None:
            return False
        cur_str = cur_node.substr
        while word_i < len(word):
            if word[word_i] != cur_str[cur_str_i]:
                return False
            word_i += 1
            cur_str_i += 1
            if cur_str_i < len(cur_str):
                continue
            if word_i == len(word):
                if cur_node.is_terminal:
                    return True
                return False
            cur_node, cur_str_i = cur_node.children.get(word[word_i]), 0
            if cur_node is None:
                return False
            cur_str = cur_node.substr
        return False

    def suggest(self, word: str):
        lowered = word[:].lower()
        if self.last_searched_for == lowered:
            '''
            Микрооптимизация. Прежде чем начать искать слово, проверяем, не искали ли мы его только что.
            Если да - возвращаем предыдущий результат.
            '''
            return
        self.suggests.clear()
        self.last_searched_for = lowered
        self.root.suggest(lowered, self.suggests)


def main():
    t, length, i = Trie(), int(input()), 0

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
        if t.find(line):
            print(f'{line} - ok')
            continue
        t.suggest(line)
        if t.suggests:
            # Сортирую специально в парсинге, а не внутри словаря, чтобы реализация не была заточена под вывод
            print(f'{line} -> {", ".join(sorted(t.suggests))}')
            continue
        print(f'{line} -?')


if __name__ == '__main__':
    main()
