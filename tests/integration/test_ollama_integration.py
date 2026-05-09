import requests


def test_ollama_responde():
    """Verifica que Ollama esté activo."""
    response = requests.get("http://localhost:11434/api/tags", timeout=10)

    assert response.status_code == 200

    data = response.json()
    assert "models" in data


def test_modelos_ollama_disponibles():
    """Verifica que existan modelos instalados en Ollama."""
    response = requests.get("http://localhost:11434/api/tags", timeout=10)

    assert response.status_code == 200

    data = response.json()
    models = data.get("models", [])

    assert len(models) > 0, "No hay modelos instalados en Ollama"