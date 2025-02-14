import numpy as np

def Z_t(P_t, P_a, P_b):
    if P_t < P_a:
        return P_a
    if P_t > P_b:
        return P_b
    return P_t


def IL_t(P_t, P_0, P_a, P_b):
    return (np.sqrt(Z_t(P_t, P_a, P_b)) - np.sqrt(P_0) + P_t*(1/np.sqrt(Z_t(P_t, P_a, P_b)) - 1/np.sqrt(P_0))) / (np.sqrt(P_0) - np.sqrt(P_a) + P_t*(1/np.sqrt(P_0) - 1/np.sqrt(P_b)))
