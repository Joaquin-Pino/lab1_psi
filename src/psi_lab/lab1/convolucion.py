from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def convolucion_directa(
    x: NDArray[np.float64], h: NDArray[np.float64]
) -> NDArray[np.float64]:
    """Convolucion lineal completa (largo len(x) + len(h) - 1), por definicion."""
    raise NotImplementedError


def convolucion_fft(
    x: NDArray[np.float64], h: NDArray[np.float64]
) -> NDArray[np.float64]:
    """Misma convolucion lineal, via el teorema de la convolucion."""
    raise NotImplementedError
