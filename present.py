import numpy as np


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

def mat_to_list_conv(filt: np.ndarray) -> list:
    """Converts numpy array into filtered list format."""
    dim = [0 for _ in range(filt.shape[0] + filt.shape[1] - 1)]
    for i in range(filt.shape[1]):
        for j in range(filt.shape[0]):
            dim[filt.shape[0] + i - j - 1] += 1*filt[j][i]
    return dim


def width(mat: np.ndarray) -> int:
    Width = 0
    for i in range(mat.shape[0]):
        if any(mat[i,:]):
            Width += 1
    return Width

def list_to_array(dimension_vector: list[int], socle: int) -> np.ndarray:
    hit = np.zeros([socle, len(dimension_vector) + 1 - socle])
    g = lambda x: hit.shape[0] + x[1] - x[0]
    k = 0
    while k < hit.shape[0] + hit.shape[1] - 1:
        pairing = [[i, k - i] for i in range(k + 1)]
        for i in range(len(pairing) - 1, -1, -1):
            if pairing[i][0] not in range(hit.shape[0]):
                del pairing[i]
            elif pairing[i][1] not in range(hit.shape[1]):
                del pairing[i]
        for i in pairing:
            if not any(dimension_vector):
                break
            if dimension_vector[g(i) - 1] != 0:
                hit[i[0],i[1]] = 1
                dimension_vector[g(i) - 1] -= 1
        k+=1
    return hit

def k_split(a:int, b:int, k:list[int]):
    out_1 = []
    out_2 = []
    out_3 = []
    for i in range(a):
        for j in range(b):
            if i - j < k[1]:
                out_1.append([i,j])
            elif i - j > k[0]:
                out_2.append([i,j])
            else:
                out_3.append([i,j])
    return out_1, out_2, out_3


def disconnect(matrix: np.ndarray) -> list[np.ndarray]:
    split = []
    k = 0
    while k < matrix.shape[0] + matrix.shape[1] - 1:
        pairing = [[matrix.shape[0] - 1 - i, k - i] for i in range(k+1) if -1 < (k-i) < matrix.shape[1] and -1 < (matrix.shape[0] - 1 - i) < matrix.shape[0]]
        if any([matrix[p[0],p[1]] for p in pairing]):
            pass
        else:
            split.append(k)
        k += 1
    if len(split) ==0:
        return [matrix]
    else:
        split = [-1] + split + [matrix.shape[0] + matrix.shape[1]]
        out = []
        for i in range(len(split)-1):
            J, K, L = k_split(matrix.shape[0], matrix.shape[1], [matrix.shape[0] - 1 - split[i],matrix.shape[0] - 1 - split[i+1]])
            f1 = np.copy(matrix)
            A = [f1[i[0],i[1]] for i in L]
            C = sum(A)
            if not (C== 0):
                a = np.copy(matrix)
                for i in J:
                    a[i[0],i[1]] = 0
                for j in K:
                    a[j[0],j[1]] = 0
                out.append(a)
        if len(out) == 0:
            out.append(matrix)
        return out


def mat_to_num(matrix: np.ndarray) -> np.ndarray:
    g = lambda x: matrix.shape[0] + x[1] - x[0]
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            matrix[i,j] = g([i,j])*matrix[i,j]
    return matrix


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
