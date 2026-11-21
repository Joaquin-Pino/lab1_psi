import wave
from pathlib import Path

import numpy as np
import pytest

from psi_lab.lab1 import datos


def test_cancion_sintetica_largo_rango_y_determinismo():
    fs = 8000
    t, x = datos.cancion_sintetica(3.0, fs=fs, semilla=1)
    assert len(x) == len(t) == 3 * fs
    assert np.max(np.abs(x)) <= 1.0
    _, x2 = datos.cancion_sintetica(3.0, fs=fs, semilla=1)
    _, x3 = datos.cancion_sintetica(3.0, fs=fs, semilla=2)
    assert np.array_equal(x, x2)
    assert not np.array_equal(x, x3)


def test_cancion_sintetica_frecuencia_dominante_por_nota():
    fs = 11025
    _, x = datos.cancion_sintetica(1.0, fs=fs, semilla=3, dur_nota=0.5)
    nota = x[: fs // 2]
    f = np.argmax(np.abs(np.fft.rfft(nota))) * fs / len(nota)
    assert 300 - 5 <= f <= 3000 + 5


def test_seleccionar_canciones_reproducible_y_valida():
    rutas = [f"c{i}.mp3" for i in range(20)]
    a = datos.seleccionar_canciones(rutas, 5, semilla=7)
    assert a == datos.seleccionar_canciones(reversed(rutas), 5, semilla=7)
    assert len(set(a)) == 5
    with pytest.raises(ValueError):
        datos.seleccionar_canciones(rutas, 21)


def test_leer_audio_wav(tmp_path):
    fs = 8000
    x = (0.5 * np.sin(2 * np.pi * 440 * np.arange(fs) / fs) * 32767).astype("<i2")
    ruta = tmp_path / "tono.wav"
    with wave.open(str(ruta), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(fs)
        w.writeframes(x.tobytes())
    y, fs_leida = datos.leer_audio(ruta)
    assert fs_leida == fs
    assert y.shape == (fs, 1)
    assert np.allclose(y[:, 0], x / 32768.0, atol=1e-4)


def test_directorio_datos_usa_variable_de_entorno(monkeypatch, tmp_path):
    monkeypatch.setenv("PSI_DATA_DIR", str(tmp_path))
    assert datos.directorio_datos() == tmp_path


def test_listar_canciones_filtra_extensiones(tmp_path):
    for nombre in ["b.mp3", "a.WAV", "nota.txt"]:
        (tmp_path / nombre).write_bytes(b"")
    assert [Path(p).name for p in datos.listar_canciones(tmp_path)] == ["a.WAV", "b.mp3"]
    with pytest.raises(FileNotFoundError):
        datos.listar_canciones(tmp_path / "no_existe")
