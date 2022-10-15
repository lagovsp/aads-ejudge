# Copyright Sergey Lagov 2022 lagovsp@gmail.com

import re


class Vertex:
    def __init__(self, k=None, v=None, l=None, r=None, p=None):
        self.key = k
        self.val = v
        self.left = l
        self.right = r
        self.parent = p

    def __str__(self) -> str:
        if self.parent is not None:
            return f'[{self.key} {self.val} {self.parent.key}]'
        return f'[{self.key} {self.val}]'

    def __repr__(self) -> str:
        return self.__str__()

    def search(self, k: int) -> (bool, 'Vertex'):
        if k == self.key:
            return True, self
        if k < self.key and self.left is not None:
            return self.left.search(k)
        elif self.right is not None:
            return self.right.search(k)
        return False, None

    def add(self, k: int, v: str) -> (bool, 'Vertex'):
        if k == self.key:
            return False, self
        if k < self.key:
            if self.left is None:
                self.left = Vertex(k=k, v=v, p=self)
                return True, self.left
            return self.left.add(k, v)
        if self.right is None:
            self.right = Vertex(k=k, v=v, p=self)
            return True, self.right
        return self.right.add(k, v)

    def is_left_child(self) -> bool:
        if self.parent is None:
            return False
        return self is self.parent.left


class SplayTree:
    def __init__(self, r=None):
        self.root = r

    def __search(self, k: int) -> (bool, Vertex):
        if self.root is None:
            return False, None
        return self.root.search(k)

    def __add(self, k: int, v: str) -> (bool, Vertex):
        if self.root is None:
            self.root = Vertex(k=k, v=v)
            return True, self.root
        return self.root.add(k, v)

    def __extreme(self, max=True):
        if self.root is None:
            return False, None
        cur = self.root
        while (cur.right if max else cur.left) is not None:
            cur = cur.right if max else cur.left
        self.splay(cur)
        return True, cur

    def __min(self):
        return self.__extreme(max=False)

    def __max(self):
        return self.__extreme()

    # lifts x and lowers x.parent down to the right/left
    def __rotate(self, x: Vertex, right: bool) -> Vertex:
        m = x.right if right else x.left
        p = x.parent
        if p.parent is None:
            self.root = x
        else:
            if p.is_left_child():
                p.parent.left = x
            else:
                p.parent.right = x
        x.parent = p.parent
        if right:
            x.right = p
            p.left = m
        else:
            x.left = p
            p.right = m
        p.parent = x
        if m is not None:
            m.parent = p
        return x

    @staticmethod
    def merge(lhs: 'SplayTree', rhs: 'SplayTree') -> Vertex:
        if lhs.root is None:
            return rhs.root
        if rhs.root is None:
            return lhs.root
        x = lhs.__max()[1]
        x.right = rhs.root
        if rhs.root is not None:
            rhs.root.parent = x
        return x

    def add(self, k: int, v: str):
        s = self.__add(k, v)
        if not s[0]:
            print('error')
        self.splay(s[1])

    def set(self, k: int, v: str):
        s = self.__search(k)
        if not s[0]:
            print('error')
            return
        s[1].val = v
        self.splay(s[1])

    def delete(self, k: int):
        s = self.__search(k)
        if not s[0]:
            print('error')
            return
        self.splay(s[1])
        s[1].left.parent, s[1].right.parent = None, None
        self.root = SplayTree.merge(SplayTree(r=s[1].left),
                                    SplayTree(r=s[1].right))

    def search(self, k: int):
        s = self.__search(k)
        if not s[0]:
            print('0')
            return
        self.splay(s[1])
        print(f'1 {s[1].val}')

    def print(self):
        if self.root is None:
            print('_')
            return
        verts, stop = [self.root], False
        while not stop:
            stop, next_verts, ins = True, [None] * (len(verts) * 2), [None] * len(verts)
            for i, v in enumerate(verts):
                if v is not None:
                    if v.left is not None:
                        stop = False
                        next_verts[2 * i] = v.left
                    if v.right is not None:
                        stop = False
                        next_verts[2 * i + 1] = v.right
                else:
                    next_verts[2 * i] = None
                    next_verts[2 * i + 1] = None
                ins[i] = '_' if v is None else v.__str__()
            print(' '.join(ins))
            verts = next_verts

    def min(self):
        s = self.__min()
        if not s[0]:
            print('error')
            return
        print(f'{s[1].key} {s[1].val}')

    def max(self):
        s = self.__max()
        if not s[0]:
            print('error')
            return
        print(f'{s[1].key} {s[1].val}')

    def __is_zig(self, x: Vertex) -> bool:
        if x.parent is self.root:
            return True
        return False

    def __is_zig_zig(self, x: Vertex) -> bool:
        if x.is_left_child() and x.parent is not None and x.parent.is_left_child():
            return True
        if not x.is_left_child() and x.parent is not None and not x.parent.is_left_child():
            return True
        return False

    def __is_zig_zag(self, x: Vertex) -> bool:
        if x.is_left_child() and x.parent is not None and not x.parent.is_left_child():
            return True
        if not x.is_left_child() and x.parent is not None and x.parent.is_left_child():
            return True
        return False

    def __zig(self, x) -> Vertex:
        return self.__rotate(x, True if x.is_left_child() else False)

    def __zig_zig(self, x: Vertex) -> Vertex:
        if x.is_left_child():
            self.__rotate(x.parent, True)
            return self.__rotate(x, True)
        self.__rotate(x.parent, False)
        return self.__rotate(x, False)

    def __zig_zag(self, x: Vertex) -> Vertex:
        if x.is_left_child():
            self.__rotate(x, True)
            return self.__rotate(x, False)
        self.__rotate(x, False)
        return self.__rotate(x, True)

    def splay(self, x: Vertex) -> Vertex:
        while x is not self.root:
            if self.__is_zig(x):
                x = self.__zig(x)
                continue
            if self.__is_zig_zig(x):
                x = self.__zig_zig(x)
                continue
            if self.__is_zig_zag(x):
                x = self.__zig_zag(x)
                continue
        return x


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
