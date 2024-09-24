import numpy as np


def simple_to_perm(expression: list[int], n: int) -> list[int]:
    '''Takes a simple expression in format list[int], and the number n with the
    permutation of n letters and returns the corresponding permutation giving the bottom row of the
    permutation in list[int] format.'''
    out = [i+1 for i in range(n)]
    for j in expression:
        out = out[:j-1] + [out[j]] + [out[j-1]] + out[j+1:]
    return out


def flip(perm: list[int], n: int) -> list[int]:
    '''Equivalent to sending a permutation, perm, to w_0 perm.'''
    for i in range(len(perm)):
        perm[i] = n+1 - perm[i]
    return perm


def long_1(exp: list[int], k: int) -> list[int]:
    '''Equivalent to multiplying on the right by w^{K}_0.'''
    return exp[:k][::-1] + exp[k:][::-1]


def long_2(exp: list[int], k: int) -> list[int]:
    '''Equivalent to multiplying on the left by w^{K}_0.'''
    run = [i+1 for i in range(len(exp))]
    run = long_1(run, k)
    run_dict = {i + 1: run[i] for i in range(len(run))}
    return [run_dict[i] for i in exp]


def inv(exp: list[int]) -> list[int]:
    inv_dict = {exp[i]: i+1 for i in range(len(exp))}
    return [inv_dict[j+1] for j in range(len(exp))]


def niave_expression(perm: list[int], n: int) -> list[int]:
    '''Niave algorithm for producing a simple expression for a permutation.'''
    t = []
    j = [i+1 for i in range(n)]
    for i in j[::-1]:
        if simple_to_perm(t, n)[i-1] == perm[i-1]:
            pass
        else:
            t += [i for i in range(simple_to_perm(t, n).index(perm[i-1]) + 1, i)]
    return t


def perm_concat(a: list[int], b: list[int]) -> list[int]:
    '''Computes ab as a permutation.'''
    return [a[b[i] - 1] for i in range(len(a))]


def index_to_perm(index: list[int], n: int) -> list[int]:
    return inv(index + [i+1 for i in range(n) if i + 1 not in index])

def cyclic_order(a:int, b:int, c: int, n: int):
    num = [i+1 for i in range(n)]
    num = num[c-1:] + num[:c-1]
    t1 = num.index(a)
    t2 = num.index(b)
    return t1 < t2



def perm_necklace(v:list[int] , v_perm:list[int], w:list[int], n, flip = False) -> list:
    sigma = perm_concat(inv(v_perm), w)
    out = []
    for i in range(n):
        out.append(sorted([sigma[j] for j in range(n) if cyclic_order(sigma[j], j+1, i + 1, n)]))
    for j in range(n):
        if j + 1 == sigma[j] and (j + 1) in v:
            out = [sorted(a + [j + 1]) for a in out]
    if flip:
        out_flip = []
        for i in out:
            out_flip.append(sorted([inv(sigma)[j-1] for j in i]))
        return out_flip
    else:
         return out


def s_sb_w(v:list[int],v_perm:list[int],w:list[int], n:int) -> list[list[int]]:
    sigma = perm_concat(w, inv(v_perm))
    out = []
    for i in range(n):
        out.append(sorted([j+1 for j in range(n) if cyclic_order(j+1, sigma[j], i + 1, n)]))
    for j in range(n):
        if j + 1 == sigma[j] and (j + 1) in v:
            out = [sorted(a + [j + 1]) for a in out]
    out1 = []
    for i in out:
        out1.append(sorted([inv(v_perm)[j-1] for j in i]))
    return out1

import itertools as it

def matroid(necklace:list[list[int]]) -> list[list[int]]:
    k = len(necklace[0])
    n = len(necklace)
    N = [cyclic_min(necklace,c,n) for c in range(n)]
    S = [list(b) for b in it.combinations([i+1 for i in range(n)],k)]
    remove = []
    for s in S:
        for i in range(n):
            c = [i+1 for i in range(n)][i:] + [i+1 for i in range(n)][:i]
            test = True
            s = sorted(s, key=lambda x: c.index(x))
            p = sorted(N[i], key=lambda x: c.index(x))
            for j in range(k):
                if cyclic_order(p[j], s[j], i + 1, n) or p[j] == s[j]:
                    pass
                else:
                    test = False
                    break
            if not test:
                remove.append(sorted(s))
    _, indices = np.unique(remove, return_index=True, axis = 0)
    r = [remove[i] for i in indices]
    for a in r:
        del S[S.index(a)]
    return S

def cyclic_min(l1: list[list[int]], c:int, n:int):
    b = [i + 1 for i in range(n)][c:] + [i + 1 for i in range(n)][:c]
    l2 = map(lambda i: sorted(i, key=lambda y: b.index(y)), l1)
    l3 = [list(j) for j in list(l2)]
    k = len(l3[0])
    p = []
    for s in l3:
        worked = True
        for i in range(k):
            for j in l3:
                if not cyclic_order(s[i], j[i], c + 1, n) and s[i] != j[i]:
                    worked = False
        if worked:
            p.append(sorted(s))
    if len(p) != 0:
        return p[0]
    else:
        print('No minimum found')


def weakly_seperated(q:list[int], w:list[int]) -> bool:
    l1 = q.copy()
    l2 = w.copy()
    n = max(l1 + l2)
    ws = False
    for i in range(n):
        if i+1 in l1 and i+1 in l2:
            del l1[l1.index(i+1)]
            del l2[l2.index(i+1)]
    if len(l1) == 0:
        ws = True
    else:
        for j in range(n):
            b = [i+1 for i in range(n)][j:] + [i+1 for i in range(n)][:j]
            if (max([b.index(y) for y in l1]) < min([b.index(z) for z in l2])) or (max([b.index(y) for y in l2]) < min([b.index(z) for z in l1])):
                ws = True
    return ws








