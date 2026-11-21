import numpy as np


def muestrear(fun, fs, duracion):
    """
    Evalúa fun(t) en t = n / fs, n = 0..N-1. Retorna (t, x).
    """
    dt = 1.0 / fs
    N = int(np.ceil(duracion * fs))
    t = np.arange(N) * dt
    x = fun(t)
    return t, x

def frecuencia_alias(f, fs):
    """
    Calcula la frecuencia aparente en [0, fs/2] de una senoidal de f Hz muestreada a fs.
    """
    return np.abs((f + fs / 2) % fs - fs / 2)