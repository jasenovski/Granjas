import numpy as np

def mmq(entradas: np.array, saidas: np.array, g: int):

    s_x = []
    for i in range(2 * g, -1, -1):
        s_x.append(sum(entradas ** i))

    M = []
    for j in range(g, -1, -1):
        l = [s_x[-i - j] for i in range(1, g + 2)]
        M.append(l[::-1])
    
    M = np.array(M)
    
    M_inv = np.linalg.inv(M)

    s_xy = []
    for k in range(g, -1, -1):
        s_xy.append(sum((entradas ** k) * saidas))

    s_xy = np.array(s_xy).reshape(g + 1, 1)

    coeficientes = np.linalg.multi_dot([M_inv, s_xy])

    return coeficientes
