import os
import time
import requests
import pytest
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = os.getenv("MCP_EPIIS_URL", "http://127.0.0.1:5008")

TEST_USER = os.getenv("MCP_TEST_USER", "admin")
TEST_PASS = os.getenv("MCP_TEST_PASS", "password123")

USUARIOS_CONCURRENTES = [50, 100, 200, 300]

RUTAS = [
    "/dashboard",
    "/documentos",
    "/consultar",
    "/generar",
    "/web",
    "/academico",
]

REPETICIONES_POR_USUARIO = 3
ESTADOS_VALIDOS = {200, 302, 401, 403}


def percentil_95(tiempos):
    tiempos = sorted(tiempos)
    if not tiempos:
        return 0
    indice = int(len(tiempos) * 0.95) - 1
    indice = max(0, min(indice, len(tiempos) - 1))
    return tiempos[indice]


def simular_usuario(usuario_id):
    resultados = []

    with requests.Session() as session:
        # Intento de login
        try:
            inicio = time.perf_counter()
            response = session.post(
                f"{BASE_URL}/login",
                data={
                    "username": TEST_USER,
                    "password": TEST_PASS,
                },
                timeout=10,
                allow_redirects=False,
            )
            duracion = time.perf_counter() - inicio

            resultados.append({
                "usuario": usuario_id,
                "ruta": "/login",
                "estado": response.status_code,
                "tiempo": duracion,
                "error": response.status_code >= 500,
            })

        except Exception:
            resultados.append({
                "usuario": usuario_id,
                "ruta": "/login",
                "estado": "ERROR",
                "tiempo": 10,
                "error": True,
            })

        # Navegación por rutas principales
        for _ in range(REPETICIONES_POR_USUARIO):
            for ruta in RUTAS:
                try:
                    inicio = time.perf_counter()
                    response = session.get(
                        f"{BASE_URL}{ruta}",
                        timeout=10,
                        allow_redirects=False,
                    )
                    duracion = time.perf_counter() - inicio

                    resultados.append({
                        "usuario": usuario_id,
                        "ruta": ruta,
                        "estado": response.status_code,
                        "tiempo": duracion,
                        "error": response.status_code not in ESTADOS_VALIDOS,
                    })

                except Exception:
                    resultados.append({
                        "usuario": usuario_id,
                        "ruta": ruta,
                        "estado": "ERROR",
                        "tiempo": 10,
                        "error": True,
                    })

    return resultados


@pytest.mark.parametrize("cantidad_usuarios", USUARIOS_CONCURRENTES)
def test_carga_real_usuarios_concurrentes(cantidad_usuarios):
    inicio_total = time.perf_counter()
    resultados = []

    with ThreadPoolExecutor(max_workers=cantidad_usuarios) as executor:
        tareas = [
            executor.submit(simular_usuario, usuario_id)
            for usuario_id in range(1, cantidad_usuarios + 1)
        ]

        for tarea in as_completed(tareas):
            resultados.extend(tarea.result())

    duracion_total = time.perf_counter() - inicio_total

    total_peticiones = len(resultados)
    total_errores = sum(1 for r in resultados if r["error"])
    tiempos = [r["tiempo"] for r in resultados]

    promedio = sum(tiempos) / len(tiempos)
    maximo = max(tiempos)
    p95 = percentil_95(tiempos)
    porcentaje_error = (total_errores / total_peticiones) * 100
    peticiones_por_segundo = total_peticiones / duracion_total

    print("\n--- RESULTADO DE PRUEBA DE CARGA REAL ---")
    print(f"Usuarios concurrentes: {cantidad_usuarios}")
    print(f"Peticiones ejecutadas: {total_peticiones}")
    print(f"Errores detectados: {total_errores}")
    print(f"Porcentaje de error: {porcentaje_error:.2f}%")
    print(f"Tiempo total: {duracion_total:.3f} s")
    print(f"Tiempo promedio: {promedio:.3f} s")
    print(f"Tiempo máximo: {maximo:.3f} s")
    print(f"Percentil 95: {p95:.3f} s")
    print(f"Peticiones por segundo: {peticiones_por_segundo:.2f}")

    assert porcentaje_error <= 5.0
    assert promedio < 3.0
    assert p95 < 5.0