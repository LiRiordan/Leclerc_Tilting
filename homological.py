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



def submodules(hit: np.ndarray) -> list:
    sub = []
    g = lambda x: hit.shape[0] + x[1] - x[0]
    for i in range(hit.shape[0]):
        for j in range(hit.shape[1]):
            if hit[i,j] ==0:
                pass
            else:
                s = np.copy(hit[:i+1,:j+1])
                for r in range(s.shape[1] -1, -1, -1):
                    if not any(s[:,r]):
                        s = np.delete(s,r,axis = 1)
                for t in range(s.shape[0] -1, -1, -1):
                    if not any(s[t,:]):
                        s = np.delete(s, t, axis = 0)
                sub.append([s, g([i,j]), [i,j]])
    return sub


def quotients(hit: np.ndarray) -> list:
    quot = []
    g = lambda x: hit.shape[0] + x[1] - x[0]
    for i in range(hit.shape[0]):
        for j in range(hit.shape[1]):
            if hit[i,j] ==0:
                pass
            else:
                q = np.copy(hit[i:,j:])
                for r in range(q.shape[1] -1, -1, -1):
                    if not any(q[:,r]):
                        q = np.delete(q,r,axis = 1)
                for t in range(q.shape[0] -1, -1, -1):
                    if not any(q[t,:]):
                        q = np.delete(q, t, axis = 0)
                quot.append([q,g([i+q.shape[0] - 1,j+q.shape[1] - 1])])
    return quot


def max_quotient(profiles_1, profiles_2):
    new =[]
    for j in profiles_2:
        k = submodules(j)
        for t in profiles_1:
            for l in quotients(t):
                for m in k:
                    if np.array_equal(l[0], m[0]) and l[1] == m[1]:
                        pos = m[2]
                        j[:pos[0] + 1,:pos[1] + 1] = 0
        new.append(j)
    return new

def lec_to_cmc(profiles):
    out = []
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

### Need to convert, also add the normal v^{-1}w necklace one
