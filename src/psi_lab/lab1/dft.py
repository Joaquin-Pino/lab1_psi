def dft(x):
    """DFT por definicion, O(N^2): X[k] = sum_n x[n] exp(-2j pi k n / N)."""
    raise NotImplementedError

def idft(X):
    """DFT inversa por definicion."""
    raise NotImplementedError

def espectro(x, fs, ventana="rect", nfft=None):
    """Espectro de amplitud de un lado. ventana en {"rect", "hann", "hamming"};
    nfft > len(x) rellena con ceros. Retorna (freqs, amp)."""
    raise NotImplementedError