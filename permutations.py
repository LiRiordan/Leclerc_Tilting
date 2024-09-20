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
        out.append([sigma[j] for j in range(n) if cyclic_order(sigma[j], j+1, i + 1, n)])
    for j in range(n):
        if j + 1 == sigma[j] and (j + 1) in v:
            out = [sorted(a + [j + 1]) for a in out]
    if flip:
        out_flip = []
        for i in out:
            out_flip.append([inv(sigma)[j-1] for j in i])
        return out_flip
    else:
         return out



