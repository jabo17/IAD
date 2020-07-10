"""
 "An optimal algorithm for generating minimal perfect hash functions"
 Based on Zbigniew J. Czech, George Havas and Bohdan S. Majewski
 This is a python implementation of the described perfect hash function
 with an example for mapping city names in germany to integers
"""
from typing import List, Any
import random
import json

FILE_CITIES = "entfernungen.json";
WORD_LENGTH = 30


class PerfectHash:
    _T1: List[int] = []
    _T2: List[int] = []

    _n = 0  # n = cm
    _m = 0  # len(values)

    # graph (adjacency list)
    _G = []
    # edges
    _E = dict()

    # [0,n-1] -> [0,m-1]
    # V -> [0,m-1]
    _g_assignment = []

    def __init__(self, values):
        self._m = len(values)
        self._n = int(self._m * 2 + 1)
        # step 1: map T1,T2 and G,E
        self._generate_acyclic_G(values)
        # step 2: assignment for g
        self._traverse()

    def __call__(self, w: str) -> int:
        u = self._f1(w)
        v = self._f2(w)
        return (self._g(u) + self._g(v)) % self._m;

    def _f1(self, w):
        u = 0
        for j in range(len(w)):
            u += self._T1[j] * ord(w[j])
        return u % self._n

    def _f2(self, w):
        v = 0
        for j in range(len(w)):
            v += self._T2[j] * ord(w[j])
        return v % self._n

    def _g(self, node):
        return self._g_assignment[node]

    def _traverse(self):
        self._g_assignment = [0] * self._n
        visited = [False] * len(self._G)

        def visit(node):
            if not visited[node]:
                visited[node] = True
                for neighbor in self._G[node]:
                    if not visited[neighbor]:
                        h = 0
                        if (node, neighbor) in self._E:
                            h = self._E[(node, neighbor)]
                        else:
                            h = self._E[(neighbor, node)]
                        self._g_assignment[neighbor] = (h - self._g(node)) % self._m

                        visit(neighbor)

        for node in range(len(self._G)):
            if not visited[node] and len(self._G[node]) > 0:
                visit(node)

        # we assigned [0,n-1] to [0,m-1]
        # so we don't need the mappings anymore
        del self._G
        del self._E

    def _generate_acyclic_G(self, W):
        while PerfectHash.is_acyclic(self._G):
            self._G = [[] for i in range(self._n)]
            self._E = dict()
            self._T1 = PerfectHash.randomly_generate_table(self._n)
            self._T2 = PerfectHash.randomly_generate_table(self._n)
            for i in range(len(W)):
                u = self._f1(W[i])
                v = self._f2(W[i])
                if v==u and v not in self._G[u] and u not in self._G[v]:
                    self._G = []
                    break
                self._G[u].append(v)
                self._G[v].append(u)
                self._E[(u, v)] = i % self._m

    @staticmethod
    def is_acyclic(G):
        if len(G) == 0:
            return True
        visited = [False] * len(G)

        def visit(node, from_node):
            if not visited[node]:
                visited[node] = True
                for neighbor in G[node]:
                    if neighbor == from_node:
                        continue
                    if visit(neighbor, node):
                        return True
                return False
            else:
                return True

        for node in range(len(G)):
            if not visited[node] and len(G[node]) > 0:
                if visit(node, node):
                    return True
        return False

    @staticmethod
    def randomly_generate_table(n):
        return [random.randint(0, n - 1) for i in range(WORD_LENGTH)]


def import_city_names():
    with open(FILE_CITIES, 'r', encoding="utf-8") as file:
        cities = json.load(fp=file)

    return cities


def test_perfect_hash():
    cities = import_city_names()
    citynames = [name for name, value in cities.items()]

    for i in range(1):
        perfecthashf = PerfectHash(citynames)

        for i in range(len(citynames)):
            #print(f"{perfecthashf(citynames[i])} - {citynames[i]}")
            if i < len(citynames)-1:
                assert perfecthashf(citynames[i]) < perfecthashf(citynames[i+1])
            #assert i == perfecthashf(citynames[i])

        print(perfecthashf._T1)
        print(perfecthashf._T2)
        print(perfecthashf._g_assignment)

        print(perfecthashf("Hamburg"))
        print(citynames[perfecthashf("Hamburg")])