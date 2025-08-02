import pytest
from fastapi.testclient import TestClient
from response_engine.engine import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.skip(reason="Requires a valid OpenAI API Key and mock response logic.")
def test_generate_response_success():
    """Test the /generate endpoint with a mock successful response."""
    # In a real-world scenario, you would mock the OpenAI API call
    # For now, we'll assume it returns a successful response.
    request_data = {
        "intent": "greet",
        "slots": {}
    }
    response = client.post("/generate", json=request_data)
    assert response.status_code == 200
    assert "response" in response.json()
    assert isinstance(response.json()["response"], str)

def test_generate_response_invalid_request():
    """Test the /generate endpoint with an invalid request."""
    response = client.post("/generate", json={"invalid_field": "data"})
    assert response.status_code == 422 # Unprocessable Entity
    
def test_load_prompt_template_not_found_fallback():
    """Test that the load function falls back to a default template."""
    from response_engine.engine import load_prompt_template
    # This will load the default template since 'non_existent_template' doesn't exist
    template = load_prompt_template("non_existent_template")
    assert "你是一個企業級 AI 助理" in template
