import numpy as np
from homological import top, socle
from permutations import simple_to_perm, perm_concat, niave_expression, long_1
from present import width, profile_decorator

def epsilon(w_expression: list[int], n: int) -> list:
    """Given a reduced expression for w we return the string as above giving
    the filtration of the projective-injectives after applying epsilon.
    WARNING: Leclerc often applies w^{-1}w_0 rather than w. This requires
    the user to compute a reduced expression for w^{-1}w_0 before using this function."""
    Epsilon = []
    Projectives = []
    for i in range(n):
        P = np.ones([i+1,n-i])
        Projectives.append(P)
    for P in Projectives:
        expression = w_expression.copy()
        while len(expression) > 0:
            head = top(P)
            g = lambda x: P.shape[0] + x[1] - x[0]
            for t in head:
                if g(t) == expression[-1]:
                    P[t[0],t[1]] = 0
            del expression[-1]
        Epsilon.append(P)
    return Epsilon


@profile_decorator
def proj_inj(v_expression: list[int], w_expression: list[int], n: int, show = False) -> list:
    """Given a reduced expression for w and v we return the projective injectives in Leclerc's categorification"""
    inv_w = simple_to_perm(w_expression[::-1], n)
    u = perm_concat(inv_w, [i+1 for i in range(n)][::-1])
    u_expression = niave_expression(u, n)
    Epsilon_Dagger = []
    for P in epsilon(u_expression, n-1):
        expression = v_expression.copy()[::-1]
        while len(expression) > 0:
            socles = socle(P)
            g = lambda x: P.shape[0] + x[1] - x[0]
            for t in socles:
                if g(t) == expression[-1]:
                    P[t[0],t[1]] = 0
            del expression[-1]
        Epsilon_Dagger.append(P)
    return Epsilon_Dagger


def width_set(w_expression: list[int], k: int, n: int) -> list[int]:
    long = niave_expression(long_1([i+1 for i in range(n)], k), n)
    S = proj_inj(long, w_expression, n, show = False)
    return [width(J) for J in S]


def necklace(profiles, v: list[int], widths: list[int]) -> list[list]:
    '''Given a k index, v, and a simple expression for a permutation, w, such that the Schubert cell X_w contains X_v
    we perform Leclerc's epsilon and epsilon dagger functors to produce the projective injectives in Leclerc's
    category C_{v,w}.

    These are then used to produce a list of rank one modules in JKS's CM(C) such that they are
    mapped to Leclerc's modules via pi_v.

    We always also include the module M_v by default which can (in general) have
    extensions with the lifts of Leclerc's projective injectives.'''
    Necklace= []
    for t in range(len(profiles)):
        J = profiles[t]
        g = lambda x: J.shape[0] + x[1] - x[0]
        tops = [i for i in sorted(top(J), key = lambda r : r[0], reverse= True)]
        if len(tops) == 0:
            pass
        else:
            x = [i[0] for i in sorted(top(J), key = lambda r : r[0], reverse=True)]
            splice = []
            for j in range(len(x) - 1):
                splice += [g(tops[j]) + t + 1 for t in range(abs(x[j+1] - x[j]))]
            splice += [g(tops[-1]) + t + 1 for t in range(abs(x[-1] + 1))]
            ind = [i+1 for i in range(len(v) - widths[t])]
            splice = ind + splice
            Necklace.append([max(i,j) for (i,j) in zip(splice,v)])
    return Necklace