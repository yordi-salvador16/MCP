import os
import time
import requests
import pytest

BASE_URL = os.getenv("MCP_EPIIS_URL", "http://127.0.0.1:5008")

# Tiempo máximo permitido por ruta en entorno de laboratorio
MAX_RESPONSE_TIME = 3.0


@pytest.mark.parametrize("ruta", [
    "/login",
    "/dashboard",
    "/documentos",
    "/consultar",
    "/generar",
    "/web",
    "/academico",
])
def test_tiempo_respuesta_rutas_principales(ruta):
    """Verifica que las rutas principales respondan en un tiempo aceptable."""
    inicio = time.perf_counter()

    response = requests.get(
        f"{BASE_URL}{ruta}",
        timeout=10,
        allow_redirects=False
    )

    duracion = time.perf_counter() - inicio

    print(f"Ruta: {ruta} | Estado: {response.status_code} | Tiempo: {duracion:.3f} s")

    assert response.status_code != 500
    assert duracion < MAX_RESPONSE_TIME


def test_promedio_respuesta_login():
    """Verifica el tiempo promedio de respuesta del login."""
    tiempos = []

    for _ in range(5):
        inicio = time.perf_counter()

        response = requests.get(
            f"{BASE_URL}/login",
            timeout=10,
            allow_redirects=False
        )

        duracion = time.perf_counter() - inicio
        tiempos.append(duracion)

        assert response.status_code == 200

    promedio = sum(tiempos) / len(tiempos)

    print(f"Tiempo promedio del login: {promedio:.3f} s")

    assert promedio < 2.0


def test_estabilidad_peticiones_repetidas_login():
    """Verifica que varias peticiones seguidas al login no generen error interno."""
    for i in range(5):
        response = requests.get(
            f"{BASE_URL}/login",
            timeout=10,
            allow_redirects=False
        )

        print(f"Petición {i + 1}: estado {response.status_code}")

        assert response.status_code == 200
        assert response.status_code != 500