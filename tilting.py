from present import list_to_array, disconnect
from permutations import niave_expression, long_2, index_to_perm, perm_concat, inv
from leclerc import epsilon
from homological import max_quotient, index_from_v

def reflector(expression: list[int], n: int) -> list[int]:
    """We follow the algorithm in the Leclerc paper on cluster structures in
    strata of Grassmannians and treat a:list[int] as the indices for a reduced
    expression of the permutation w.
    We start by considering the fundamental weight omega_a[-1]. We then act by the reflection a[-1].
    This gives omega_a[-1] + alpha_a[-1].
    We then delete a[-1] and apply the new a[-1] to this sum as a reflection until the list is empty.
    We assume we are in type A. The integer n records the number of vertices.
    """
    a = expression.copy()
    for i in range(len(a)):
        a[i] -= 1
    root = a[-1]
    counter = [0 for _ in range(n)]
    while len(a) > 0:
        counter[a[-1]] = -counter[a[-1]]
        if a[-1] == root:
            counter[a[-1]] += 1
        if a[-1] - 1 > -1:
            counter[a[-1]] += counter[a[-1] - 1]
        if a[-1] + 1 < n:
            counter[a[-1]] += counter[a[-1] + 1]
        del a[-1]
    return counter



def tilt_alg_gls(expression: list[int], n: int) -> list:
    """We now implement Leclerc's algorithm by taking sequential subwords of the reduced
    expression for w and applying the above process. This gives a tilting object in C_{w}"""
    total = []
    reversed_expression = expression[::-1]
    for i in range(len(expression)):
        total.append([reflector(reversed_expression[:i+1], n), reversed_expression[i]])
    return [list_to_array(j[0], j[1]) for j in total]


def tilter(v: list[int], w_expression: list[int], k: int, n: int) -> list:
    t_modules = []
    T_modules = []
    J = tilt_alg_gls(w_expression, n - 1)
    v_adapt = perm_concat(inv(long_2(index_to_perm(v, n), k)), [i+1 for i in range(n)][::-1])
    v_exp = niave_expression(v_adapt, n)
    F = epsilon(v_exp, n - 1)
    hits = max_quotient(F,J)
    for h in hits:
        t_modules += disconnect(h)
    for i in t_modules:
        T_modules.append(index_from_v(v, i))
    while v in T_modules:
        T_modules.remove(v)
    return T_modules
