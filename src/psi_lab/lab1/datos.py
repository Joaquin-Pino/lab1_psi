"""Obtención de datos para el caso aplicado (mini-Shazam).

- Listado y selección reproducible de las canciones que el usuario deja en
  ``<PSI_DATA_DIR>/musica``.
- Lectura de audio a arreglos NumPy (pydub/ffmpeg como decodificador auxiliar).
- Generador de "canciones" sintéticas (secuencias de tonos) para tests y CI.

Los datos nunca se versionan: quedan en ``PSI_DATA_DIR`` (por defecto ``./data``).
"""

from __future__ import annotations

import os
import random
from collections.abc import Iterable, Sequence
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

SEMILLA_POR_DEFECTO = 13318


def directorio_datos() -> Path:
    """Carpeta de datos: variable de entorno ``PSI_DATA_DIR`` o ``./data``."""
    return Path(os.environ.get("PSI_DATA_DIR", "data"))


def leer_audio(ruta: str | os.PathLike[str]) -> tuple[NDArray[np.float64], int]:
    """
    Lee un archivo de audio (wav, mp3, ...) a un arreglo float64 en [-1, 1].

    Retorna (x, fs): x con forma (n_muestras, n_canales), fs en Hz.
    Los formatos distintos de wav requieren ffmpeg en el sistema.
    """
    from pydub import AudioSegment

    seg = AudioSegment.from_file(str(ruta))
    datos = np.array(seg.get_array_of_samples(), dtype=np.float64)
    datos = datos.reshape(-1, seg.channels)
    datos /= float(1 << (8 * seg.sample_width - 1))
    return datos, seg.frame_rate


def seleccionar_canciones(
    rutas: Iterable[str | os.PathLike[str]], n: int, semilla: int = SEMILLA_POR_DEFECTO
) -> list[str]:
    """Elige n rutas de forma reproducible (orden alfabético + semilla fija)."""
    rutas = sorted(str(r) for r in rutas)
    if n > len(rutas):
        raise ValueError(f"se piden {n} canciones pero hay {len(rutas)}")
    return sorted(random.Random(semilla).sample(rutas, n))


def listar_canciones(
    carpeta: str | os.PathLike[str] | None = None,
    extensiones: Sequence[str] = (".mp3", ".wav", ".flac", ".ogg"),
) -> list[str]:
    """
    Lista (ordenadas) las canciones que el usuario dejó en ``carpeta``
    (por defecto ``directorio_datos() / "musica"``). No descarga nada.
    """
    carpeta = Path(carpeta) if carpeta is not None else directorio_datos() / "musica"
    if not carpeta.is_dir():
        raise FileNotFoundError(f"no existe la carpeta de música: {carpeta}")
    return sorted(str(p) for p in carpeta.iterdir() if p.suffix.lower() in extensiones)


def cancion_sintetica(
    duracion: float,
    fs: int = 11025,
    semilla: int = 0,
    dur_nota: float = 0.25,
    f_min: float = 300.0,
    f_max: float = 3000.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    "Canción" sintética: secuencia de tonos puros de ``dur_nota`` s con frecuencias
    aleatorias (semilla fija) en [f_min, f_max] Hz. Retorna (t, x) con x en [-1, 1].
    """
    rng = np.random.default_rng(semilla)
    n_notas = int(np.ceil(duracion / dur_nota))
    n_por_nota = round(dur_nota * fs)
    frecs = rng.uniform(f_min, f_max, size=n_notas)
    t_nota = np.arange(n_por_nota) / fs
    x = np.concatenate([np.sin(2 * np.pi * f * t_nota) for f in frecs])
    n = round(duracion * fs)
    x = x[:n]
    return np.arange(len(x)) / fs, x
