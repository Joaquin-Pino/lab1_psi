import numpy as np
import pytest

from psi_lab.lab1.muestreo import (
    frecuencia_alias,
    frecuencia_medida,
    muestrear,
    tabla_alias,
    tabla_alias_markdown,
)


@pytest.mark.parametrize("f", [3, 7, 13, 23])
def test_frecuencia_medida_coincide_con_alias(f):
    fs = 20.0
    _, x = muestrear(lambda t: np.sin(2 * np.pi * f * t + 0.3), fs, 2.0)
    assert frecuencia_medida(x, fs) == pytest.approx(frecuencia_alias(f, fs), abs=0.05)


@pytest.mark.parametrize("fs", [20.0, 50.0, 100.0])
def test_tabla_alias_fs_variable(fs):
    filas = tabla_alias(fs=fs, duracion=4.0)
    assert len(filas) == 4
    for fila in filas:
        assert fila["fs"] == fs
        assert fila["f_predicha"] == pytest.approx(frecuencia_alias(fila["f"], fs))
        assert fila["error"] < 0.05


def test_tabla_alias_markdown():
    md = tabla_alias_markdown(tabla_alias())
    assert md.count("\n") == 5  # encabezado + separador + 4 filas
    assert "| 13 | 20 | 7.000" in md
