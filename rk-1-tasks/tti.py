from collections import deque


class BinVertex:
    def __init__(self, p=None, v=None, l=None, r=None):
        self.parent = p
        self.left = l
        self.right = r
        self.val = v

    def __repr__(self):
        if self.val is None:
            return 'None'
        return f'{self.val}'


def desc_evens(root: BinVertex):
    s = deque()  # actually stack
    cur = root
    evens = []
    while True:
        print(f'now {cur}')
        if cur is not None:
            s.append(cur)
            print(f'put {cur}, s = {list(s)}')
            cur = cur.right
            continue
        el = s.pop()
        if el.val % 2 == 0:
            evens.append(el.val)
        print(f'evens = {evens}')
        cur = el.left
        if cur is None and not s:
            break
    print(evens)


def n_parents_l(p: BinVertex, c1, c2):
    p.left = c1
    p.right = c2
    if c1 is not None:
        c1.parent = p
    if c2 is not None:
        c2.parent = p


if __name__ == '__main__':
    n1 = BinVertex(v=38)
    n2 = BinVertex(v=15)
    n3 = BinVertex(v=40)
    n4 = BinVertex(v=31)
    n5 = BinVertex(v=60)
    n6 = BinVertex(v=2)
    n7 = BinVertex(v=70)
    n8 = BinVertex(v=80)
    n9 = BinVertex(v=100)  # root
    n10 = BinVertex(v=102)
    n11 = BinVertex(v=105)
    n12 = BinVertex(v=110)
    n13 = BinVertex(v=107)

    n_parents_l(n9, n7, n10)
    n_parents_l(n7, n6, n8)
    n_parents_l(n6, None, n5)
    n_parents_l(n5, n4, None)
    n_parents_l(n4, n2, n3)
    n_parents_l(n3, n1, None)

    n_parents_l(n10, None, n11)
    n_parents_l(n11, None, n12)
    n_parents_l(n12, n13, None)

    desc_evens(n9)
