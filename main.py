debug = True


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



def gap(filt: list[int]) -> list[int]:
    """Reformats lists in a useful way for presenting simple filtrations."""
    out = []
    out.append(filt[0] + 3)
    for j in range(1,len(filt)):
        out.append(filt[j] - filt[j-1] - 1)
    return out



def filtration(dimension_vector: list[int], socle: int) -> list:
    simples = dimension_vector.copy()
    filtration = [[socle]]
    simples[socle - 1] -= 1
    while any(simples):
        counter_list = []
        for j in filtration[-1]:
            if j < len(simples):
                if simples[j] > 0:
                    counter_list.append(j + 1)
            if j > 1:
                if simples[j - 2] > 0:
                    counter_list.append(j - 1)
        indices = set(counter_list)
        layer = sorted([i for i in indices])
        filtration.append(layer)
        for k in layer:
            simples[k - 1] -= 1
    return filtration



def list_to_profile(dimension_vector: list[int], socle: int, print_filt = False) -> str:
    """Converts filtrations into a string 'displaying' that filtration."""
    filtred = filtration(dimension_vector,socle)
    string_out = f' '
    for t in range(len(filtred)-1, -1, -1):
        for j in range(len(filtred[t])):
            string_out += f' '*gap(filtred[t])[j]
            if filtred[t][j] != 0:
                string_out += f'{filtred[t][j]}'
            else:
                string_out += ' '
        string_out += '\n '
    if print_filt:
        print(string_out)
    return string_out[:-1]



def tilt_alg_gls(expression: list[int], n: int) -> None:
    """We now implement Leclerc's algorithm by taking sequential subwords of the reduced
    expression for w and applying the above process. This gives a tilting object in C_{w}"""
    total = []
    reversed_expression = expression[::-1]
    for i in range(len(expression)):
        total.append([reflector(reversed_expression[:i+1], n), reversed_expression[i]])
    for j in total:
        print(list_to_profile(j[0], j[1]))
        print('-----------------------------------------------------------')



import numpy as np
def top(presentation) -> list:
    """Given a matrix representing a simple filtration we find the positions we allow to be removed by epsilon."""
    k = presentation.shape[0] + presentation.shape[1] - 2
    tops = []
    while k > -1:
        pairing = [[i,k-i] for i in range(k+1)]
        for i in range(len(pairing)-1,-1,-1):
            if pairing[i][0] not in range(presentation.shape[0]):
                del pairing[i]
            elif pairing[i][1] not in range(presentation.shape[1]):
                del pairing[i]
        for i in pairing:
            above = np.copy(presentation[i[0]:, i[1]:])
            above[0,0] = 0
            if not above.any():
                if presentation[i[0]][i[1]] != 0:
                    tops.append(i)
        k -= 1
    return tops



def socle(presentation) -> list:
    """Given a matrix representing a simple filtration we find the positions we allow to be removed by epsilon_dagger."""
    k = 0
    socles = []
    while k < presentation.shape[0] + presentation.shape[1] - 1:
        pairing = [[i,k-i] for i in range(k+1)]
        for i in range(len(pairing)-1,-1,-1):
            if pairing[i][0] not in range(presentation.shape[0]):
                del pairing[i]
            elif pairing[i][1] not in range(presentation.shape[1]):
                del pairing[i]
        for i in pairing:
            above = np.copy(presentation[:i[0] + 1, :i[1] + 1])
            above[i[0],i[1]] = 0
            if not above.any():
                if presentation[i[0]][i[1]] != 0:
                    socles.append(i)
        k += 1
    return socles



def mat_to_list_conv(filt: np.ndarray) -> list:
    """Converts numpy array into filtered list format."""
    dim = [0 for _ in range(filt.shape[0] + filt.shape[1] - 1)]
    for i in range(filt.shape[1]):
        for j in range(filt.shape[0]):
            dim[filt.shape[0] + i - j - 1] += 1*filt[j][i]
    return dim


def profile_decorator(func):
    def wrapper(v_expression: list[int], w_expression: list[int], n: int):
        counter = []
        for j in func(v_expression, w_expression, n):
            counter.append(mat_to_list_conv(j))
        for j in counter:
            list_to_profile(j, counter.index(j) + 1, print_filt=True)
        return func(v_expression, w_expression, n), counter
    return wrapper



def epsilon(w_expression: list[int], n: int, debug = False) -> list:
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
    if debug:
        for J in Epsilon:
            print(J)
    return Epsilon



def index_to_perm(index: list[int], n: int) -> list[int]:
    return inv(index + [i+1 for i in range(n) if i + 1 not in index])



# @profile_decorator
def proj_inj(v_expression: list[int], w_expression: list[int], n: int, debug = False) -> list:
    """Given a reduced expression for w and v we return the projective injectives in Leclerc's categorification"""
    inv_w = simple_to_perm(w_expression[::-1], n)
    u = perm_concat(inv_w, [i+1 for i in range(n)][::-1])
    u_expression = niave_expression(u, n)
    Epsilon_Dagger = []
    for P in epsilon(u_expression, n-1, debug):
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


def necklace(profiles, v: list[int], debug = False) -> set:
    Necklace= []
    for J in profiles:
        g = lambda x: J.shape[0] + x[1] - x[0]
        tops = [i for i in sorted(top(J), key = lambda r : r[0], reverse= True)]
        if debug:
            print(J)
        if len(tops) == 0:
            pass
        else:
            x = [i[0] for i in sorted(top(J), key = lambda r : r[0], reverse=True)]
            splice = []
            for j in range(len(x) - 1):
                splice += [g(tops[j]) + t + 1 for t in range(abs(x[j+1] - x[j]))]
            splice += [g(tops[-1]) + t + 1 for t in range(abs(x[-1] + 1))]
            ind = [i+1 for i in range(len(v) - len(splice))]
            splice = ind + splice
            if debug:
                print(splice)
            Necklace.append([max(i,j) for (i,j) in zip(splice,v)])
    Necklace = [v] + Necklace
    return set(Necklace)




def main(w_expression: list[int], v: list[int], k: int, n: int, Projective_Injective = False, Tilting = False, Necklace = False, Galashin_Lam = False) -> None:
    """Given a reduced expression for w and a k-index v giving rise to a Grassmannian
    Richardson variety in Gr(k,n+1) we return useful information about the categorifications.

     In particular Projective_Injective = True produces the projective-injective objects
     in Leclerc's category.

     Tilting = True performs an algorithm found in Leclerc's paper giving rise to a cluster tilting object in Leclerc's
     category.

     Necklace = True returns the necklace which porjects down onto Leclerc's projective injectives under the
     functor pi_v.

     Galashin_Lam = True uses a slightly different convention as described in the paper 'Positroid varieties and
     cluster algebras'. When Galashin_Lam = True we convert their permutations to the Leclerc conventions and perform any computations there."""
    if Necklace:
        Projective_Injective = True
    if Galashin_Lam:
        hold = v.copy()
        v = sorted(inv(flip(simple_to_perm(w_expression[::-1], n + 1), n + 1))[:k])
        w_expression = niave_expression(flip(simple_to_perm(hold[::-1],n + 1), n+1), n+1)
    if Projective_Injective:
        v_expression = niave_expression(long_2(index_to_perm(v, n+1), k), n+1)
        pi = proj_inj(v_expression, w_expression, n+1, debug)
        if Necklace:
            print(necklace(pi, v, debug))
    if Tilting:
        print('First we produce the cluster-tilting object in C_w \n')
        tilt_alg_gls(w_expression, n)
        print('Each summand must then be quotiented by a maximal submodule which is a factor of the following module:')
        v_adapt = niave_expression(long_2(index_to_perm(v, n+1), k), n+1)
        counter = []
        for j in epsilon(v_adapt,n):
            counter.append(mat_to_list_conv(j))
        for j in counter:
            list_to_profile(j, counter.index(j) + 1, print_filt=True)



# w_expression =  niave_expression(long_2(index_to_perm([3,6], 6), 2), 6)
# v = [1,3]
v = [4,3,2,1,4,3,2,7,6,5,4,3,8,6,4,10,9,8,7,6,5,11,10,9,8,7]
w_expression = [4,3,2,1,5,4,3,2,7,6,5,4,3,8,7,6,5,4,10,9,8,7,6,5,11,10,9,8,7,6]
k = 6
n = 11
Projective_Injective = False
Tilting = False
Necklace = True
Galashin_Lam = True


if __name__ == '__main__':
    main(w_expression, v, k, n, Projective_Injective, Tilting, Necklace, Galashin_Lam)


### Getting much closer!!!
### Current issue stemming from adding indeices prior or after!!


































