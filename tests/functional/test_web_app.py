import os
import requests

BASE_URL = os.getenv("MCP_EPIIS_URL", "http://127.0.0.1:5008")


def test_servidor_web_responde():
    """Verifica que el servidor web esté activo."""
    response = requests.get(f"{BASE_URL}/login", timeout=10)
    assert response.status_code == 200


def test_login_carga_correctamente():
    """Verifica que la página de login cargue."""
    response = requests.get(f"{BASE_URL}/login", timeout=10)
    assert response.status_code == 200
    assert "login" in response.text.lower() or "usuario" in response.text.lower()


def test_dashboard_responde_sin_error_servidor():
    """Verifica que dashboard responda sin error 500."""
    response = requests.get(f"{BASE_URL}/dashboard", timeout=10, allow_redirects=False)
    assert response.status_code in [200, 302, 401, 403]


def test_documentos_responde_sin_error_servidor():
    """Verifica que documentos responda sin error 500."""
    response = requests.get(f"{BASE_URL}/documentos", timeout=10, allow_redirects=False)
    assert response.status_code in [200, 302, 401, 403]


def test_consultar_responde_sin_error_servidor():
    """Verifica que consultar responda sin error 500."""
    response = requests.get(f"{BASE_URL}/consultar", timeout=10, allow_redirects=False)
    assert response.status_code in [200, 302, 401, 403]


def test_generar_responde_sin_error_servidor():
    """Verifica que generar responda sin error 500."""
    response = requests.get(f"{BASE_URL}/generar", timeout=10, allow_redirects=False)
    assert response.status_code in [200, 302, 401, 403]


def test_web_responde_sin_error_servidor():
    """Verifica que el módulo web responda sin error 500."""
    response = requests.get(f"{BASE_URL}/web", timeout=10, allow_redirects=False)
    assert response.status_code in [200, 302, 401, 403]


def test_academico_responde_sin_error_servidor():
    """Verifica que el módulo académico responda sin error 500."""
    response = requests.get(f"{BASE_URL}/academico", timeout=10, allow_redirects=False)
    assert response.status_code in [200, 302, 401, 403]
