import os
import requests
import pytest

BASE_URL = os.getenv("MCP_EPIIS_URL", "http://127.0.0.1:5008")


def request_get(path):
    """Realiza una petición GET sin seguir redirecciones."""
    return requests.get(f"{BASE_URL}{path}", timeout=10, allow_redirects=False)


def request_post(path, data=None, files=None):
    """Realiza una petición POST sin seguir redirecciones."""
    return requests.post(
        f"{BASE_URL}{path}",
        data=data or {},
        files=files,
        timeout=10,
        allow_redirects=False,
    )


@pytest.mark.parametrize("ruta", [
    "/dashboard",
    "/documentos",
    "/consultar",
    "/generar",
    "/web",
    "/academico",
])
def test_rutas_de_usuario_requieren_autenticacion(ruta):
    """Verifica que las rutas principales no permitan acceso libre sin sesión."""
    response = request_get(ruta)

    assert response.status_code in [302, 401, 403], (
        f"La ruta {ruta} debería redirigir o bloquear acceso sin sesión, "
        f"pero respondió {response.status_code}"
    )


@pytest.mark.parametrize("ruta", [
    "/admin/dashboard",
    "/admin/usuarios",
    "/admin/documentos",
    "/admin/fuentes-web",
])
def test_rutas_de_administrador_requieren_autenticacion(ruta):
    """Verifica que las rutas administrativas estén protegidas sin sesión."""
    response = request_get(ruta)

    assert response.status_code in [302, 401, 403], (
        f"La ruta administrativa {ruta} debería estar protegida, "
        f"pero respondió {response.status_code}"
    )


@pytest.mark.parametrize("ruta", [
    "/upload",
    "/generar/crear",
    "/web/add",
    "/academico/chat",
])
def test_operaciones_post_sin_sesion_no_generan_error_servidor(ruta):
    """Verifica que operaciones POST sin sesión no generen error interno."""
    response = request_post(ruta)

    assert response.status_code != 500, (
        f"La ruta {ruta} generó error interno del servidor"
    )


def test_login_con_credenciales_invalidas_no_rompe_servidor():
    """Verifica que un intento de login inválido no genere error 500."""
    response = request_post("/login", data={
        "username": "usuario_invalido",
        "password": "clave_invalida",
    })

    assert response.status_code != 500


def test_api_usuarios_sin_sesion_no_genera_error_servidor():
    """Verifica que la API de usuarios no genere error 500 sin sesión."""
    response = request_get("/api/usuarios")

    assert response.status_code != 500


def test_descarga_documento_inexistente_no_genera_error_servidor():
    """Verifica que la descarga de un documento inexistente no rompa el servidor."""
    response = request_get("/documentos/999999/download")

    assert response.status_code != 500