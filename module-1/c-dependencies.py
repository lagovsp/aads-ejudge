# Copyright Sergey Lagov 2022 lagovsp@gmail.com

class Vertex:
    def __init__(self, name, vul=False, dir=False):
        self.name = name
        self.linked_to = set()  # vertices
        self.depends_on = set()  # vertices
        self.vul = vul
        self.dir = dir


class Graph:
    def __init__(self):
        self.__vertexes = dict()  # names to vertices
        self.__vuls = set()  # vulnerable vertices' names

    def get_vuls(self) -> set:
        return self.__vuls

    def get_vertex(self, name) -> Vertex:
        return self.__vertexes.get(name)

    def add_vertex_linked(self, vname, lname):
        self.__add_if_absent_by_name(vname).linked_to.add(self.__add_if_absent_by_name(lname))

    def add_vertex_depends(self, vname, dname):
        self.__add_if_absent_by_name(vname).depends_on.add(self.__add_if_absent_by_name(dname))

    def __add_if_absent_by_name(self, name) -> Vertex:
        v = self.get_vertex(name)
        if v is None:
            v = self.add_vertex(Vertex(name))
        return v

    def add_vertex(self, v: Vertex):
        self.__vertexes.update({v.name: v})
        if v.vul:
            self.__vuls.add(v.name)
        return self.__vertexes[v.name]


def get_paths_to_directs(v: Vertex, curp: list, paths: list, seen=None):
    if seen is None:
        seen = set()
    if v.name in seen:
        return
    seen.add(v.name)
    if v.dir:
        paths.append(curp[::-1])
    if not v.linked_to:
        return
    neighbours = v.linked_to
    for neigh in neighbours:
        np = curp.copy()
        np.append(neigh.name)
        get_paths_to_directs(neigh, np, paths, seen=seen.copy())


def main():
    g = Graph()
    try:
        line = input()  # reading vulnerable libs
    except EOFError:
        return
    if not line:
        return
    vulns = line.split()
    for vuln in vulns:
        g.add_vertex(Vertex(vuln, vul=True))

    try:
        line = input()  # reading direct dependencies
    except EOFError:
        return
    if not line:
        return
    directs = line.split()
    for direct in directs:
        g.add_vertex(Vertex(direct, dir=True))

    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            continue
        arr = line.split()
        lib = arr[0]
        for base in arr[1:]:
            g.add_vertex_linked(base, lib)
            g.add_vertex_depends(lib, base)

    answers = []
    vulns = g.get_vuls()
    for vuln in vulns:
        get_paths_to_directs(g.get_vertex(vuln), [vuln], answers)
    for answer in answers:
        print(' '.join(answer))


if __name__ == '__main__':
    main()
