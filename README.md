# Faculty Hub Backend Algoritmo

Este repositorio contiene el backend algoritmo de la plataforma Faculty Hub, implementado en Python usando FastAPI. Se encarga de realizar la asignación óptima de docentes a dictados utilizando la librería OR-Tools de Google.

## Tecnologías utilizadas

- Python
- FastAPI
- OR-Tools (para la optimización de asignaciones)
- Docker (para contenerización)

## Herramientas de desarrollo

Para garantizar la consistencia y calidad del código, utiliza las siguientes herramientas:

### Formateador Black

Instalar el formateador Black:

```
pip install black
```

### Linter Pylint

Instalar pylint para análisis estático de código:

```
pip install pylint
```

### Ordenador de imports isort

Instalar isort para ordenar los imports automáticamente:

```
pip install isort
```

### Pre-commit

Instalar pre-commit para ejecutar verificaciones antes de cada commit:

```
pip install pre-commit
pre-commit install
```

Cada vez que realices un commit, el pre-commit ejecutará automáticamente Black, isort y pylint sobre tu código.

## Desarrollo en Docker

### Requisitos

Tener Docker instalado

### Ejecutar el servicio en modo observación:

```
docker compose watch
```

### Abrir una terminal del contenedor en otra terminal:

```
docker exec -it <container_name> ../bin/bash
```

Ejemplo:

```
docker exec -it matching_algorithm-app-1 ../bin/bash
```

### Detener el servicio:

```
docker compose down
```

### Construir la imagen Docker:

```
docker build -t my-python-app .
```

### Ejecutar el contenedor:

```
docker run -it my-python-app
```

### Guardar versiones de las librerías:

```
pip freeze > requirements.txt
```

### Ejecutar la API

```
uvicorn src.app:app --reload
```

### Crear el entorno virtual e instalar dependencias

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Ejecutar los test

Activate el ambiente de python donde estan intaladas las librerias

```
python -m unittest discover -s tests
```

Para ejecutar los test que simulan casos reales de asignación docentes con datos aleatorios:

```
python tests/matching_algorithm_test/simulate_real_scenario.py
```

## Despliegue

El backend algoritmo se despliega en AWS utilizando contenedores Docker.

## Colaboración

Para contribuir, sigue el archivo CONTRIBUTING.md y asegúrate de seguir las prácticas de desarrollo establecidas.
