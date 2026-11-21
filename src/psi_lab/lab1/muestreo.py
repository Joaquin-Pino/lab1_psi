from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray


def muestrear(
    fun: Callable[[NDArray[np.float64]], NDArray[np.float64]],
    fs: float,
    duracion: float,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    Evalúa fun(t) en t = n / fs, n = 0..N-1. Retorna (t, x).
    """
    dt = 1.0 / fs
    N = int(np.ceil(duracion * fs))
    t = np.arange(N) * dt
    x = fun(t)
    return t, x


def frecuencia_alias(
    f: float | NDArray[np.float64], fs: float
) -> float | NDArray[np.float64]:
    """
    Calcula la frecuencia aparente en [0, fs/2] de una senoidal de f Hz muestreada a fs.
    """
    return np.abs((f + fs / 2) % fs - fs / 2)


def frecuencia_medida(x: NDArray[np.float64], fs: float) -> float:
    """
    Estima la frecuencia aparente (Hz, en [0, fs/2]) de una senoidal muestreada,
    SIN usar la DFT: busca la f que mejor ajusta por minimos cuadrados el modelo
    x[n] ~ a cos(2 pi f n / fs) + b sin(2 pi f n / fs) + c.

    Barrido grueso en [0, fs/2] y dos refinamientos locales.

    TODO(PC2-1): cuando `espectro` / `dft` esten implementadas, se puede reemplazar
    por la frecuencia del pico de `espectro(x, fs, ventana="hann", nfft=...)`.
    Mientras tanto este ajuste evita depender de ellas.
    """
    x = np.asarray(x, dtype=float)
    n = np.arange(len(x))

    def error(f: float) -> float:
        w = 2 * np.pi * f / fs * n
        A = np.column_stack([np.cos(w), np.sin(w), np.ones_like(w)])
        coef = np.linalg.lstsq(A, x, rcond=None)[0]
        return float(np.sum((x - A @ coef) ** 2))

    grilla = np.linspace(0.0, fs / 2, 8 * len(x) + 1)
    paso = grilla[1] - grilla[0]
    mejor = grilla[int(np.argmin([error(f) for f in grilla]))]
    for _ in range(2):
        local = np.linspace(max(mejor - paso, 0.0), min(mejor + paso, fs / 2), 41)
        mejor = local[int(np.argmin([error(f) for f in local]))]
        paso = local[1] - local[0]
    return float(mejor)


def tabla_alias(
    frecuencias: tuple[float, ...] = (3, 7, 13, 23),
    fs: float = 20.0,
    duracion: float = 2.0,
) -> list[dict[str, float]]:
    """
    Tabla de PC1-2: muestrea senoidales de cada f en `frecuencias` (Hz) a `fs` (Hz)
    durante `duracion` (s) y compara la frecuencia medida con la predicha por
    `frecuencia_alias`. Cada fila: f, fs, f_predicha, f_medida, error (todo en Hz).
    """
    filas = []
    for f in frecuencias:
        _, x = muestrear(lambda t, f=f: np.sin(2 * np.pi * f * t + 0.3), fs, duracion)
        predicha = float(frecuencia_alias(f, fs))
        medida = frecuencia_medida(x, fs)
        filas.append(
            {
                "f": float(f),
                "fs": float(fs),
                "f_predicha": predicha,
                "f_medida": medida,
                "error": abs(medida - predicha),
            }
        )
    return filas


def tabla_alias_markdown(filas: list[dict[str, float]]) -> str:
    """Formatea las filas de `tabla_alias` como tabla Markdown (Hz)."""
    lineas = [
        "| f (Hz) | fs (Hz) | f predicha (Hz) | f medida (Hz) | error (Hz) |",
        "|---|---|---|---|---|",
    ]
    for r in filas:
        lineas.append(
            f"| {r['f']:g} | {r['fs']:g} | {r['f_predicha']:.3f} "
            f"| {r['f_medida']:.3f} | {r['error']:.3f} |"
        )
    return "\n".join(lineas)
