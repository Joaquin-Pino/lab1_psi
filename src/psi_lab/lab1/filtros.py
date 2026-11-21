from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def fir_pasabajos(
    fc: float, fs: float, n_coef: int, ventana: str = "hamming"
) -> NDArray[np.float64]:
    """Sinc truncada y enventanada, normalizada a ganancia 1 en DC."""
    raise NotImplementedError


def fir_pasaaltos(
    fc: float, fs: float, n_coef: int, ventana: str = "hamming"
) -> NDArray[np.float64]:
    raise NotImplementedError


def fir_pasabanda(
    f1: float, f2: float, fs: float, n_coef: int, ventana: str = "hamming"
) -> NDArray[np.float64]:
    raise NotImplementedError


def fir_rechazabanda(
    f1: float, f2: float, fs: float, n_coef: int, ventana: str = "hamming"
) -> NDArray[np.float64]:
    raise NotImplementedError


def respuesta_frecuencia(
    h: NDArray[np.float64], fs: float, n: int = 4096
) -> tuple[NDArray[np.float64], NDArray[np.complex128]]:
    """Retorna (freqs, H) con H complejo."""
    raise NotImplementedError


def filtrar(x: NDArray[np.float64], h: NDArray[np.float64]) -> NDArray[np.float64]:
    """Aplica h a x (largo igual a x), compensando el retardo (n_coef - 1) / 2."""
    raise NotImplementedError
