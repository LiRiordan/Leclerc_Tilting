import numpy as np
from present import index_from_v, disconnect


def top(presentation:np.ndarray) -> list:
    """Given a matrix representing a simple filtration we find the positions we allow to be removed by epsilon."""
    k = presentation.shape[0] + presentation.shape[1] - 2
    tops = []
    while k > -1:
        pairing = [[presentation.shape[0] - 1 - i, k - i] for i in range(k+1) if -1 < (k-i) < presentation.shape[1] and -1 < (presentation.shape[0] - 1 - i) < presentation.shape[0]]
        for i in pairing:
            above = np.copy(presentation[i[0]:, i[1]:])
            above[0,0] = 0
            if not above.any():
                if presentation[i[0]][i[1]] != 0:
                    tops.append(i)
        k -= 1
    return tops



def socle(presentation: np.ndarray) -> list:
    """Given a matrix representing a simple filtration we find the positions we allow to be removed by epsilon_dagger."""
    k = 0
    socles = []
    while k < presentation.shape[0] + presentation.shape[1] - 1:
        pairing = [[presentation.shape[0] - 1 - i, k - i] for i in range(k+1) if -1 < (k-i) < presentation.shape[1] and -1 < (presentation.shape[0] - 1 - i) < presentation.shape[0]]
        for i in pairing:
            above = np.copy(presentation[:i[0] + 1, :i[1] + 1])
            above[i[0],i[1]] = 0
            if not above.any():
                if presentation[i[0]][i[1]] != 0:
                    socles.append(i)
        k += 1
    return socles

def profile_decorator(func):
    def wrapper(profiles_1: list[np.ndarray], profiles_2: list[np.ndarray], v:list[int]):
        counter = []
        out = []
        for j in func(profiles_1, profiles_2, v):
            counter += disconnect(j)
        for j in counter:
            out += [index_from_v(v, j)]
        return func(profiles_1, profiles_2, v), out
    return wrapper



def clear(s: np.ndarray) -> np.ndarray:
    for r in range(s.shape[1] - 1, -1, -1):
        if not any(s[:, r]):
            s = np.delete(s, r, axis=1)
    for t in range(s.shape[0] - 1, -1, -1):
        if not any(s[t, :]):
            s = np.delete(s, t, axis=0)
    return s



def kill(mat: np.ndarray, index: list[int]) -> np.ndarray:
    cmat = np.copy(mat)
    cmat[index[0],index[1]] = 0
    return cmat



def list_slam(l:list) -> list[int]:
    out = []
    for i in l:
        out += i
    return out



def submodules(hit: np.ndarray) -> list:
    sub = [hit]
    a = hit.copy()
    if not np.any(a):
        return []
    else:
        t = top(a)
        for i in t:
            sub += submodules(kill(a,i))
        g = [list_slam(sorted(top(a))) for a in sub]
        indices = [g.index(list(l)) for l in set(map(tuple, g))]
        sub = [sub[i] for i in indices]
        return sub



def quotients(hit: np.ndarray) -> list:
    quot = [hit]
    a = hit.copy()
    if not np.any(a):
        return []
    else:
        s = socle(a)
        for j in s:
            quot += quotients(kill(a,j))
        g = [list_slam(sorted(socle(a))) for a in quot]
        indices = [g.index(list(l)) for l in set(map(tuple, g))]
        quot = [quot[i] for i in indices]
        return quot

def simple_quotients(hit: np.ndarray) -> list:
    g = lambda x: hit.shape[0] - x[0] + x[1]
    sim_soc_quot = [[np.copy(hit), g([0,0])]]
    for i in range(hit.shape[0]):
        for j in range(hit.shape[1]):
            if hit[i,j] == 0:
                pass
            else:
                a = hit.copy()
                for l in range(i):
                    a[:l+1,:] = 0
                for k in range(j):
                    a[:,:k+1] = 0
                sim_soc_quot.append([a,g([i,j])])
    return sim_soc_quot


def socle_quotients(hit: np.ndarray, socle: int) -> list:
    pairing = []
    for i in range(hit.shape[0]):
        for j in range(hit.shape[1]):
            if j - i == socle - hit.shape[0]:
                pairing.append([i,j])
    out = []
    for p in pairing:
        if hit[p[0],p[1]] ==0:
            pass
        else:
            a = hit.copy()
            for l in range(p[0]):
                a[l, :] = 0
            for k in range(p[1]):
                a[:, k] = 0
            out.append(clear(a))
    return out


def mat_combine(m1:np.ndarray, m2:np.ndarray) -> np.ndarray:
    B = np.zeros([m1.shape[0], m1.shape[1]])
    for i in range(m1.shape[0]):
        for j in range(m2.shape[1]):
            if m1[i,j] != 0 and m2[i,j] != 0:
                B[i,j] = 1
    return B





@profile_decorator
def simple_max_quotient(profiles_1: list[np.ndarray], profiles_2: list[np.ndarray], v:list[int]) -> list[np.ndarray]:
    new = []
    for j in profiles_2:
        start = [np.copy(j)]
        for t in profiles_1:
            q = socle_quotients(t, j.shape[0])
            run = True
            while len(q) > 0 and run:
                m = q[0]
                if m.shape[0] <= j.shape[0] and m.shape[1] <= j.shape[1]:
                    a = top(m)
                    if all([j[i[0],i[1]] for i in a]):
                        l = []
                        for c in range(m.shape[0]):
                            for d in range(m.shape[1]):
                                if m[c,d] == 1:
                                    l.append([c,d])
                        N = np.copy(j)
                        for h in l:
                            N[h[0],h[1]] = 0
                        start.append(N)
                        run = False
                del q[0]
        M = start[0]
        del start[0]
        while len(start) > 0:
            M = mat_combine(M,start[0])
            del start[0]
        new.append(M)
    return new


@profile_decorator
def max_quotient(profiles_1:list[np.ndarray], profiles_2:list[np.ndarray], v:list[int]) -> list[np.ndarray]:
    new =[]
    for j in profiles_2:
        g1 = lambda x: j.shape[0] + x[1] - x[0]
        for t in profiles_1:
            g2 = lambda x: t.shape[0] + x[1] - x[0]
            q = quotients(t)
            for l in q:
                for m in submodules(j):
                    a = [g1(i) for i in top(m)]
                    b = [g2(k) for k in top(l)]
                    if np.array_equal(clear(l), clear(m)) and a==b:
                        for i in top(m):
                            j[:i[0] + 1,:i[1] + 1] = 0
        new.append(j)
    return new



