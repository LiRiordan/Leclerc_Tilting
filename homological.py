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


def clear(s: np.ndarray):
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



def submodules(hit: np.ndarray) -> list:
    sub = [hit]
    a = hit.copy()
    if not np.any(a):
        return []
    else:
        t = top(a)
        for i in t:
            sub += submodules(kill(a,i))
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
        return quot


def max_quotient(profiles_1, profiles_2):
    new =[]
    for j in profiles_2:
        g1 = lambda x: j.shape[0] + x[1] - x[0]
        for t in profiles_1:
            g2 = lambda x: t.shape[0] + x[1] - x[0]
            for l in quotients(t):
                for m in submodules(j):
                    a = [g1(i) for i in top(m)]
                    b = [g2(k) for k in top(l)]
                    if np.array_equal(clear(l), clear(m)) and a == b:
                        for i in top(m):
                            j[:i[0] + 1,:i[1] + 1] = 0
        new.append(j)
    return new


def index_from_v(v:list[int], matrix: np.ndarray) -> list[int]:
    t = v.copy()
    g = lambda x: matrix.shape[0] + x[1] - x[0]
    for i in range(matrix.shape[0]):
        hits = np.unique([g([i,j])*matrix[i,j] for j in range(len(matrix[i,:]))])
        if any(hits):
            if hits[0] == 0:
                low = hits[1]
            else:
                low = hits[0]
            high = hits[-1]
            m = v.index(low)
            t[m] = int(high) + 1
    return t

