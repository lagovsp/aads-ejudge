import re


class Vertex:
    def __init__(self):
        self.k = None
        self.v = None
        self.l = None
        self.r = None
        self.p = None

    def __str__(self) -> str:
        if self.p is not None:
            return f'[{self.k} {self.v} {self.p.k}]'
        return f'[{self.k} {self.v}]'

    def search(self, k: int):
        if k == self.k:
            return self
        if k < self.k and self.l is not None:
            return self.l.search(k)
        elif self.r is not None:
            return self.r.search(k)
        return None


class BinaryTree:
    def __init__(self):
        self.root = None

    def search(self, k: int):
        return self.root.search(k)


class SplayTree(BinaryTree):
    def __init__(self):
        super().__init__()
        self.min = None  # vertex
        self.max = None  # vertex

    def add(self, k: int, v: str):  # special for splay trees
        pass

    def set(self, k: int, v: str):
        x = super().search(k)
        if x is None:
            return
        x.v = v
        self.__splay(x)

    def delete(self, k: int):
        x = super().search(k)
        self.__splay(x)
        # merge of x's sons

    def search(self, k: int):
        x = super().search(k)
        if x is None:
            return '0'
        self.__splay(x)
        return f'1 {x.v}'

    def min(self):
        pass

    def max(self):
        pass

    def print(self):
        if self.root is None:
            print('_')
            return
        l = []  # next level

    def __splay(self, x):
        pass

    def __split(self):
        pass


def main():
    st = SplayTree()
    methods = {
        'add': SplayTree.add,
        'set': SplayTree.set,
        'delete': SplayTree.delete,
        'search': SplayTree.search,
        'min': SplayTree.min,
        'max': SplayTree.max,
        'print': SplayTree.print,
    }

    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            continue

        if re.match(r'^(min|max|print)$', line):
            methods[line](st)
            continue
        if re.match(r'^(delete|search) (0|(-?[1-9]\d*))$', line):
            c, k = line.split()
            methods[c](st, int(k))
            continue
        if re.match(r'^(add|set) (0|(-?[1-9]\d*)) \S+$', line):
            c, k, v = line.split()
            methods[c](st, int(k), v)
            continue

        print('error')


if __name__ == '__main__':
    main()
