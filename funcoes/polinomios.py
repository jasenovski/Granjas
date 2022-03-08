def polinomio(coefs, entrada):
    grau = len(coefs) - 1
    f = 0
    for i in range(grau, -1, -1):
        f += coefs[grau - i] * entrada ** i
    
    return f