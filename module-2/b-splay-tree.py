# Copyright Sergey Lagov 2022 lagovsp@gmail.com

import re


class Node:
    def __init__(self, k=None, v=None, l=None, r=None, p=None):
        self.key = k
        self.val = v
        self.left = l
        self.right = r
        self.parent = p

    def search(self, k: int) -> (bool, 'Node'):
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

    def add(self, k: int, v: str) -> (bool, 'Node'):
        cur = self
        while True:
            if k == cur.key:
                return False, cur
            if k < cur.key:
                if cur.left is None:
                    cur.left = Node(k=k, v=v, p=cur)
                    return True, cur.left
                cur = cur.left
                continue
            if cur.right is None:
                cur.right = Node(k=k, v=v, p=cur)
                return True, cur.right
            cur = cur.right

    def is_left_child(self) -> bool:
        if self.parent is None:
            return False
        return self is self.parent.left


class SplayTree:
    def __init__(self, r=None):
        self.root = r

    def __search(self, k: int) -> (bool, Node):
        if self.root is None:
            return False, None
        return self.root.search(k)

    def __add(self, k: int, v: str) -> (bool, Node):
        if self.root is None:
            self.root = Node(k=k, v=v)
            return True, self.root
        return self.root.add(k, v)

    def __extreme(self, max=True) -> (bool, Node):
        if self.root is None:
            return False, None
        cur = self.root
        while (cur.right if max else cur.left) is not None:
            cur = cur.right if max else cur.left
        return True, cur

    def __min(self) -> (bool, Node):
        return self.__extreme(max=False)

    def __max(self) -> (bool, Node):
        return self.__extreme()

    def __rotate(self, x: Node, right: bool) -> Node:
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
    def merge(lhs: 'SplayTree', rhs: 'SplayTree') -> Node:
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
        lhs.__splay(node)
        node.right = rhs.root
        rhs.root.parent = node
        return node

    def add(self, k: int, v: str):
        status, node = self.__add(k, v)
        self.__splay(node)
        if not status:
            raise Exception('adding present element')

    def set(self, k: int, v: str):
        status, node = self.__search(k)
        self.__splay(node)
        if not status:
            raise Exception('setting absent element')
        node.val = v

    def delete(self, k: int):
        status, node = self.__search(k)
        self.__splay(node)
        if not status:
            raise Exception('deleting absent element')
        self.root = SplayTree.merge(SplayTree(r=node.left),
                                    SplayTree(r=node.right))

    def search(self, k: int) -> (bool, Node):
        status, node = self.__search(k)
        self.__splay(node)
        if not status:
            return False, None
        return True, node

    def min(self) -> Node:
        status, node = self.__min()
        self.__splay(node)
        if not status:
            raise Exception('empty, no minimum element')
        return node

    def max(self) -> Node:
        status, node = self.__max()
        self.__splay(node)
        if not status:
            raise Exception('empty, no maximum element')
        return node

    def __is_zig(self, x: Node) -> bool:
        if x.parent is self.root:
            return True
        return False

    def __is_zig_zig(self, x: Node) -> bool:
        if x.is_left_child() and x.parent is not None and x.parent.is_left_child():
            return True
        if not x.is_left_child() and x.parent is not None and not x.parent.is_left_child():
            return True
        return False

    def __is_zig_zag(self, x: Node) -> bool:
        if x.is_left_child() and x.parent is not None and not x.parent.is_left_child():
            return True
        if not x.is_left_child() and x.parent is not None and x.parent.is_left_child():
            return True
        return False

    def __zig(self, x) -> Node:
        return self.__rotate(x, True if x.is_left_child() else False)

    def __zig_zig(self, x: Node) -> Node:
        if x.is_left_child():
            self.__rotate(x.parent, True)
            return self.__rotate(x, True)
        self.__rotate(x.parent, False)
        return self.__rotate(x, False)

    def __zig_zag(self, x: Node) -> Node:
        if x.is_left_child():
            self.__rotate(x, True)
            return self.__rotate(x, False)
        self.__rotate(x, False)
        return self.__rotate(x, True)

    def __splay(self, x: Node):
        while x is not None and x is not self.root:
            if self.__is_zig(x):
                self.__zig(x)
            elif self.__is_zig_zig(x):
                self.__zig_zig(x)
            elif self.__is_zig_zag(x):
                self.__zig_zag(x)


def print_tree(tree: SplayTree):
    cur_len, cur_layer, next_layer, stop = 1, {0: tree.root}, dict(), False
    while not stop:
        stop = True
        for i in range(cur_len):
            node = cur_layer.pop(i) if i in cur_layer else None
            if node is None:
                print('_' if i == 0 else ' _', end='')
                continue
            if node.left is not None:
                stop = False
                next_layer[i * 2] = node.left
            if node.right is not None:
                stop = False
                next_layer[i * 2 + 1] = node.right
            if node.parent is None:
                print('[{} {}]'.format(node.key, node.val), end='')
                continue
            if i == 0:
                print('[{} {} {}]'.format(node.key, node.val, node.parent.key), end='')
                continue
            print(' [{} {} {}]'.format(node.key, node.val, node.parent.key), end='')
        cur_layer, next_layer = next_layer, dict()
        cur_len *= 2
        print()


def main():
    st = SplayTree()

    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            continue
        try:
            if line == 'print':
                print_tree(st)
                continue
            if line == 'min':
                n = st.min()
                print(f'{n.key} {n.val}')
                continue
            if line == 'max':
                n = st.max()
                print(f'{n.key} {n.val}')
                continue
            if re.fullmatch(r'delete (0|(-?[1-9]\d*))', line):
                _, k = re.split(' ', line)
                st.delete(int(k))
                continue
            if re.fullmatch(r'search (0|(-?[1-9]\d*))', line):
                _, k = re.split(' ', line)
                status, n = st.search(int(k))
                print(f'1 {n.val}' if status else '0')
                continue
            if re.fullmatch(r'add (0|(-?[1-9]\d*)) .*', line):
                _, k, v = re.split(' ', line)
                st.add(int(k), v)
                continue
            if re.fullmatch(r'set (0|(-?[1-9]\d*)) .*', line):
                _, k, v = re.split(' ', line)
                st.set(int(k), v)
                continue
        except Exception:
            print('error')
            continue
        print('error')


if __name__ == '__main__':
    main()
