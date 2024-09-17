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
