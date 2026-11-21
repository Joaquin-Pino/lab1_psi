# psi-lab1

Laboratorios de Procesamiento de Señales e Imágenes (13318), USACH.

Paquete Python (`psi_lab`) con las rutinas del Laboratorio 1 "Del muestreo al filtrado":
`muestreo`, `dft`, `convolucion` y `filtros` (parte común) y el caso aplicado de
huellas de audio (`datos`, `caso_audio`). Todo el código está en `src/psi_lab/lab1/`.

> Estado: en desarrollo (rama `dev`). Las firmas existen, pero las implementaciones aún no están completas.

## Requisitos

- Python >= 3.13
- `ffmpeg` en el sistema (solo para leer audio que no sea wav; la imagen Docker ya lo incluye)
- Docker y Docker Compose (opcional, para desarrollar en contenedor)

## Instalación local

```bash
git clone https://github.com/Joaquin-Pino/lab1_psi.git
cd lab1_psi

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -e ".[dev]"          # paquete + pytest, pytest-cov y ruff
```

El proyecto usa `src` layout: `import psi_lab` solo funciona después de instalar con `pip install -e .`.
La instalación editable (`-e`) hace que los cambios en `src/` se reflejen sin reinstalar.

Para usar JupyterLab agrega el extra `notebook`: `pip install -e ".[dev,notebook]"`.

Comprobación rápida:

```bash
python -c "import psi_lab.lab1; print(psi_lab.lab1.__version__)"
```

## Tests y lint

```bash
pytest                                          # todos los tests
pytest tests/lab1/unit/test_dft.py              # un archivo
pytest tests/lab1/unit/test_dft.py::test_nombre # un test
pytest --cov=psi_lab --cov-report=term-missing  # con cobertura

ruff check .                                    # lint (lo mismo que corre el CI)
ruff format .                                   # formato
```

Los tests están en `tests/lab1/unit/` (una función a la vez) y `tests/lab1/integration/`
(flujo completo sobre señales sintéticas, sin descargas).

## Desarrollo con Docker

La imagen (`Dockerfile`) parte de `python:3.13-slim`, instala `ffmpeg` y el paquete con `pip install -e ".[dev]"`.
`compose.yaml` define dos servicios:

| Servicio | Comando | Para qué |
|----------|---------|----------|
| `tests`  | `pytest` | Correr los tests en un entorno limpio, igual al del CI |
| `lab1`   | `python -m psi_lab.lab1.caso_audio` | Descargar/generar datos y regenerar figuras y tablas en `./informe` (por ahora es un placeholder) |

```bash
docker compose build                 # construir la imagen
docker compose run --rm tests        # correr los tests en el contenedor
docker compose run --rm lab1         # regenerar figuras/tablas (se escriben en ./informe)
```

### Flujo para probar cambios

El código se copia dentro de la imagen al construirla (`COPY . .`), así que **después de editar
código hay que reconstruir** para que el contenedor lo vea:

```bash
docker compose build && docker compose run --rm tests
```

Para iterar más rápido sin reconstruir, monta el repo sobre el contenedor:

```bash
docker compose run --rm -v "$PWD":/app tests                                   # todos los tests
docker compose run --rm -v "$PWD":/app tests pytest tests/lab1/unit/test_dft.py -x   # un archivo
docker compose run --rm -v "$PWD":/app tests ruff check .                      # lint
docker compose run --rm -v "$PWD":/app tests bash                              # shell dentro del contenedor
```

Reconstruye la imagen solo cuando cambien `pyproject.toml` (dependencias) o el `Dockerfile`.

## Integración continua

`.github/workflows/ci.yml` corre en push a `main`/`dev`, en el tag `lab1` y en pull requests:

1. Instalación limpia con `pip install -e ".[dev]"`, `ruff check .` y `pytest --cov=psi_lab`.
2. Construcción de la imagen y `docker compose run --rm tests`.

Antes de abrir un PR conviene correr localmente `ruff check .` y `docker compose run --rm tests`.

## Estructura

```
src/psi_lab/lab1/   muestreo, dft, convolucion, filtros, datos, caso_audio
tests/lab1/unit/    tests unitarios (propiedades teóricas, una función a la vez)
tests/lab1/integration/  tests de flujo completo con señales sintéticas
informe/            informe (lab1.pdf) y figuras generadas
```

## Documentación de la API

_Pendiente:_ por cada función, módulo, firma, unidades y shapes de argumentos y resultados
(requerido por el enunciado para los tests del equipo docente).
