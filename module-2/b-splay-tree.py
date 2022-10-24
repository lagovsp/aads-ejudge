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

    def search(self, k: int) -> (bool, 'Vertex'):
        cur = self
        while True:
            if k == cur.key:
                return True, cur
            if k < cur.key:
                if cur.left is None:
                    return False, cur
                cur = cur.left
                continue
            if cur.right is None:
                return False, cur
            cur = cur.right

    def add(self, k: int, v: str) -> (bool, 'Vertex'):
        cur = self
        while True:
            if k == cur.key:
                return False, cur
            if k < cur.key:
                if cur.left is None:
                    cur.left = Vertex(k=k, v=v, p=cur)
                    return True, cur.left
                cur = cur.left
                continue
            if cur.right is None:
                cur.right = Vertex(k=k, v=v, p=cur)
                return True, cur.right
            cur = cur.right

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
            if rhs.root is None:
                return None
            rhs.root.parent = None
            return rhs.root
        if rhs.root is None:
            lhs.root.parent = None
            return lhs.root
        lhs.root.parent, rhs.root.parent = None, None
        node = lhs.__max()[1]
        lhs.splay(node)
        node.right = rhs.root
        rhs.root.parent = node
        return node

    def add(self, k: int, v: str):
        status, node = self.__add(k, v)
        self.splay(node)
        if not status:
            print('error')

    def set(self, k: int, v: str):
        status, node = self.__search(k)
        self.splay(node)
        if status:
            node.val = v
            return
        print('error')

    def delete(self, k: int):
        status, node = self.__search(k)
        self.splay(node)
        if not status:
            print('error')
            return
        self.root = SplayTree.merge(SplayTree(r=node.left),
                                    SplayTree(r=node.right))

    def search(self, k: int):
        status, node = self.__search(k)
        self.splay(node)
        if status:
            print(f'1 {node.val}')
            return
        print('0')

    def print(self):
        verts, stop = [self.root], False
        while not stop:
            stop, next_verts, ins = True, [None] * (len(verts) * 2), [None] * len(verts)
            for i, v in enumerate(verts):
                if v is None:
                    ins[i] = '_'
                    continue
                ins[i] = v.__str__()
                if v.left is not None:
                    stop = False
                    next_verts[2 * i] = v.left
                if v.right is not None:
                    stop = False
                    next_verts[2 * i + 1] = v.right
            print(' '.join(ins))
            verts = next_verts

    def min(self):
        status, node = self.__min()
        self.splay(node)
        if not status:
            print('error')
            return
        print(f'{node.key} {node.val}')

    def max(self):
        status, node = self.__max()
        self.splay(node)
        if not status:
            print('error')
            return
        print(f'{node.key} {node.val}')

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

    def splay(self, x: Vertex):
        while x is not None and x is not self.root:
            if self.__is_zig(x):
                self.__zig(x)
                continue
            if self.__is_zig_zig(x):
                self.__zig_zig(x)
                continue
            if self.__is_zig_zag(x):
                self.__zig_zag(x)
                continue


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
            c, k = re.split(' ', line)
            methods[c](st, int(k))
            continue
        if re.match(r'^(add|set) (0|(-?[1-9]\d*)) .*$', line):
            c, k, v = re.split(' ', line)
            methods[c](st, int(k), v)
            continue
        print('error')


if __name__ == '__main__':
    main()
