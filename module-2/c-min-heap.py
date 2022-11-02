# Copyright Sergey Lagov 2022 lagovsp@gmail.com

import math
import re


class Vertex:
    def __init__(self, k=None, v=None):
        self.key = k
        self.val = v

    @staticmethod
    def parent(i: int) -> (bool, int):
        if i == 0:
            return False, None
        return True, math.floor((i - 1) / 2)

    @staticmethod
    def children(i: int) -> (int, int):
        left = 2 * i + 1
        return left, left + 1


class MinHeap:
    def __init__(self):
        self.data = []
        self.index = dict()

    def get_node_by_index(self, i: int) -> Vertex:
        return self.data[i] if -1 < i < len(self.data) else None

    def add(self, k: int, v: str):
        if k in self.index:
            raise Exception('adding present element')
        i = len(self.data)
        self.data.append(Vertex(k=k, v=v))
        self.index.update({k: i})
        self.__sift_up(i)

    def set(self, k: int, v: str):
        i = self.index.get(k)
        if i is None:
            raise Exception('setting absent element')
        self.data[i].val = v

    def delete(self, k: int):
        i = self.index.get(k)
        if i is None:
            raise Exception('deleting absent element')
        self.__swap_vertices(i, len(self.data) - 1)
        self.index.pop(k)
        self.data.pop()
        self.__heapify(i)

    def search(self, k: int) -> int:
        '''
        Возвращает индекс найденного элемента.
        None, если элемент не был найден
        '''
        return self.index.get(k)

    def min(self) -> int:
        '''
        Возвращает индекс минимума.
        Исключение в случае пустой кучи
        '''
        if not self.data:
            raise Exception('empty, no minimum element')
        return 0

    def max(self) -> int:
        '''
        Возвращает индекс максимума.
        Исключение в случае пустой кучи
        '''
        if not self.data:
            raise Exception('empty, no maximum element')
        max_i = len(self.data) - 1
        found_par, stop = Vertex.parent(max_i)
        if found_par:
            for i in range(max_i, stop, -1):
                max_i = i if self.data[max_i].key < self.data[i].key else max_i
        return max_i

    def extract(self) -> Vertex:
        '''
        Возвращает извлекаемый (первый) элемент кучи
        '''
        if not self.data:
            raise Exception('empty, nothing to extract')
        self.__swap_vertices(0, len(self.data) - 1)
        self.index.pop(self.data[len(self.data) - 1].key)
        ret = self.data.pop()
        self.__sift_down(0)
        return ret

    def __swap_vertices(self, lhs: int, rhs: int):
        self.index.update({self.data[lhs].key: rhs})
        self.index.update({self.data[rhs].key: lhs})
        self.data[lhs], self.data[rhs] = self.data[rhs], self.data[lhs]

    def __sift_up(self, i: int):
        while i > 0:
            pi = Vertex.parent(i)[1]
            if self.data[pi].key < self.data[i].key:
                return
            self.__swap_vertices(i, pi)
            i = pi

    def __sift_down(self, i: int):
        left, right = Vertex.children(i)
        while left < len(self.data):
            min_i = left
            if right < len(self.data) and self.data[right].key < self.data[left].key:
                min_i = right
            if self.data[min_i].key > self.data[i].key:
                return
            self.__swap_vertices(i, min_i)
            i = min_i
            left, right = Vertex.children(i)

    def __heapify(self, i: int):
        if not self.data or not i < len(self.data):
            return
        found_par, pi = Vertex.parent(i)
        if found_par and self.data[i].key < self.data[pi].key:
            self.__sift_up(i)
            return
        self.__sift_down(i)


def print_heap(mh: MinHeap):
    layer, i, stop = 1, 0, False
    while not stop:
        ins, li = [None] * layer, 0
        if i + layer < len(mh.data):
            upper_bound = i + layer
        else:
            stop, upper_bound, it = True, len(mh.data), len(mh.data) - i
            while it < layer:
                ins[it] = '_'
                it += 1
        while i < upper_bound:
            v = mh.data[i]
            if i == 0:
                ins[li] = f'[{v.key} {v.val}]'
            elif li == 0:
                ins[li] = f'[{v.key} {v.val} {mh.data[v.parent(i)[1]].key}]'
            else:
                ins[li] = f'[{v.key} {v.val} {mh.data[v.parent(i)[1]].key}]'
            li += 1
            i += 1
        layer *= 2
        print(' '.join(ins))


def main():
    mh = MinHeap()

    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            continue
        try:
            if line == 'print':
                print_heap(mh)
                continue
            if line == 'min':
                i = mh.min()
                n = mh.get_node_by_index(i)
                print(f'{n.key} {i} {n.val}')
                continue
            if line == 'max':
                i = mh.max()
                n = mh.get_node_by_index(i)
                print(f'{n.key} {i} {n.val}')
                continue
            if line == 'extract':
                n = mh.extract()
                print(f'{n.key} {n.val}')
                continue
            if re.fullmatch(r'delete (0|(-?[1-9]\d*))', line):
                _, k = re.split(' ', line)
                mh.delete(int(k))
                continue
            if re.fullmatch(r'search (0|(-?[1-9]\d*))', line):
                _, k = re.split(' ', line)
                i = mh.search(int(k))
                print(f'1 {i} {mh.get_node_by_index(i).val}' if i is not None else '0')
                continue
            if re.fullmatch(r'add (0|(-?[1-9]\d*)) .*', line):
                _, k, v = re.split(' ', line)
                mh.add(int(k), v)
                continue
            if re.fullmatch(r'set (0|(-?[1-9]\d*)) .*', line):
                _, k, v = re.split(' ', line)
                mh.set(int(k), v)
                continue
        except Exception:
            print('error')
            continue
        print('error')


if __name__ == '__main__':
    main()
