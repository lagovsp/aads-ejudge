# Copyright Sergey Lagov 2022 lagovsp@gmail.com

import math
import re


class Node:
    @staticmethod
    def parent(i: int) -> (bool, int):
        if i == 0:
            return False, None
        return True, math.floor((i - 1) / 2)

    @staticmethod
    def children(i: int) -> (int, int):
        return 2 * i + 1, 2 * i + 2

    def __init__(self, k=None, v=None):
        self.key = k
        self.val = v

    def str(self, mh: 'MinHeap', i: int) -> str:
        par_found, pi = Node.parent(i)
        if not par_found:
            return f'[{self.key} {self.val}]'
        return f'[{self.key} {self.val} {mh.get_node(pi)[1].key}]'


class MinHeap:
    def __init__(self):
        self.data = []
        self.index = dict()

    def get_node(self, i: int) -> (bool, Node):
        if i < len(self.data):
            return True, self.data[i]
        return False, None

    def add(self, k: int, v: str):
        if k in self.index:
            print('error')
            return
        i = len(self.data)
        self.data.append(Node(k=k, v=v))
        self.index.update({k: i})
        self.__sift_up(i)

    def set(self, k: int, v: str):
        i = self.index.get(k)
        if i is None:
            print('error')
            return
        self.data[i].val = v

    def delete(self, k: int):
        i = self.index.get(k)
        if i is None:
            print('error')
            return
        self.__swap_nodes(i, len(self.data) - 1)
        self.index.pop(k)
        self.data.pop()
        self.__heapify(i)

    def search(self, k: int):
        i = self.index.get(k)
        if i is None:
            print('0')
            return
        print(f'1 {i} {self.data[i].val}')

    def min(self):
        if not self.data:
            print('error')
            return
        print(f'{self.data[0].key} 0 {self.data[0].val}')

    def max(self):
        if not self.data:
            print('error')
            return
        max_i = len(self.data) - 1
        found_par, stop = Node.parent(max_i)
        if found_par:
            for i in range(max_i, stop, -1):
                max_i = i if self.data[max_i].key < self.data[i].key else max_i
        print(f'{self.data[max_i].key} {max_i} {self.data[max_i].val}')

    def extract(self):
        if not self.data:
            print('error')
            return
        print(f'{self.data[0].key} {self.data[0].val}')
        self.delete(self.data[0].key)

    def print(self):
        if not self.data:
            print('_')
            return
        layer, i, stop = 1, 0, False
        while not stop:
            ins, li = ['_'] * layer, 0
            if i + layer < len(self.data):
                upper_bound = i + layer
            else:
                stop = True
                upper_bound = len(self.data)
            for it in range(i, upper_bound):
                ins[li] = self.data[i].str(self, i)
                li += 1
                i += 1
            layer *= 2
            print(' '.join(ins))

    def __swap_nodes(self, lhs: int, rhs: int):
        self.index.update({self.data[lhs].key: rhs})
        self.index.update({self.data[rhs].key: lhs})
        self.data[lhs], self.data[rhs] = self.data[rhs], self.data[lhs]

    def __sift_up(self, i: int):
        while i > 0:
            pi = Node.parent(i)[1]
            if self.data[pi].key < self.data[i].key:
                return
            self.__swap_nodes(i, pi)
            i = pi

    def __sift_down(self, i: int):
        left, right = Node.children(i)
        while left < len(self.data):
            min_i = left
            if right < len(self.data) and self.data[right].key < self.data[left].key:
                min_i = right
            if self.data[min_i].key > self.data[i].key:
                return
            self.__swap_nodes(i, min_i)
            i = min_i
            left, right = Node.children(i)

    def __heapify(self, i: int):
        if not self.data or not i < len(self.data):
            return
        found_par, pi = Node.parent(i)
        if found_par and self.data[i].key < self.data[pi].key:
            self.__sift_up(i)
            return
        left, right = Node.children(i)
        ln, rn = self.get_node(left), self.get_node(right)
        neighbours = [self.data[i].key]
        if rn[0]:
            neighbours.append(rn[1].key)
            neighbours.append(ln[1].key)
        elif ln[0]:
            neighbours.append(ln[1].key)
        if min(neighbours) != self.data[i].key:
            self.__sift_down(i)


def main():
    mh = MinHeap()
    methods = {
        'add': MinHeap.add,
        'set': MinHeap.set,
        'delete': MinHeap.delete,
        'search': MinHeap.search,
        'min': MinHeap.min,
        'max': MinHeap.max,
        'extract': MinHeap.extract,
        'print': MinHeap.print,
    }

    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            continue
        if re.match(r'^(min|max|print|extract)$', line):
            methods[line](mh)
            continue
        if re.match(r'^(delete|search) (0|(-?[1-9]\d*))$', line):
            c, k = re.split(' ', line)
            methods[c](mh, int(k))
            continue
        if re.match(r'^(add|set) (0|(-?[1-9]\d*)) .*$', line):
            c, k, v = re.split(' ', line)
            methods[c](mh, int(k), v)
            continue
        print('error')


if __name__ == '__main__':
    main()
