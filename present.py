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


def profile_decorator(func):
    def wrapper(v_expression: list[int], w_expression: list[int], n: int, show):
        if show:
            counter = []
            for j in func(v_expression, w_expression, n):
                counter.append(mat_to_list_conv(j))
            for j in counter:
                list_to_profile(j, counter.index(j) + 1, print_filt=True)
            return func(v_expression, w_expression, n), counter
        else:
            return func(v_expression, w_expression, n)
    return wrapper

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
