"""Tests for API endpoints."""

from http import HTTPStatus

from flask.testing import FlaskClient


def test_validate_valid_input(client: FlaskClient) -> None:
    """Test validation with valid CEP and vehicle type."""
    response = client.get("/api/validate?cep=01505000&vehicle_type=VUC")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["valid"] is True


def test_validate_missing_vehicle_type(client: FlaskClient) -> None:
    """Test validation without vehicle type."""
    response = client.get("/api/validate?cep=01505000")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_validate_invalid_cep(client: FlaskClient) -> None:
    """Test validation with invalid CEP format."""
    response = client.get("/api/validate?cep=abc&vehicle_type=VUC")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.get_json()
    assert data["valid"] is False


def test_fm_lookup_with_results(client: FlaskClient) -> None:
    """Test FM lookup returning results for a CEP in range."""
    response = client.get("/api/fm?cep=01505000&vehicle_type=VUC")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["count"] >= 1
    assert len(data["results"]) >= 1
    assert data["results"][0]["TIPO_VEICULO"] == "VUC"


def test_fm_lookup_all_vehicles(client: FlaskClient) -> None:
    """Test FM lookup without vehicle filter returns all types for CEP."""
    response = client.get("/api/fm?cep=01505000")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["count"] >= 1


def test_fm_lookup_not_found(client: FlaskClient) -> None:
    """Test FM lookup with CEP outside any range."""
    response = client.get("/api/fm?cep=99999999&vehicle_type=VUC")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_lm_not_found_when_no_table(client: FlaskClient) -> None:
    """Test LM endpoint returns not found when LM table doesn't exist."""
    response = client.get("/api/lm?cep=01505000&vehicle_type=VUC")
    assert response.status_code == HTTPStatus.NOT_FOUND
