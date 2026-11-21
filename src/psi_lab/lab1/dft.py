from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def dft(x: NDArray[np.float64] | NDArray[np.complex128]) -> NDArray[np.complex128]:
    """DFT por definicion, O(N^2): X[k] = sum_n x[n] exp(-2j pi k n / N)."""
    raise NotImplementedError


def idft(X: NDArray[np.complex128]) -> NDArray[np.complex128]:
    """DFT inversa por definicion."""
    raise NotImplementedError


def espectro(
    x: NDArray[np.float64], fs: float, ventana: str = "rect", nfft: int | None = None
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Espectro de amplitud de un lado. ventana en {"rect", "hann", "hamming"};
    nfft > len(x) rellena con ceros. Retorna (freqs, amp)."""
    raise NotImplementedError
