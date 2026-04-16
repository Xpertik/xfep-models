"""Tests for Client model."""

from xfep.models.client import Client


class TestClient:
    def test_minimal_client(self):
        """Minimal client for boleta — only required fields."""
        client = Client(
            tipo_documento="1",
            numero_documento="72345678",
            razon_social="Juan Perez",
        )
        assert client.tipo_documento == "1"
        assert client.numero_documento == "72345678"
        assert client.razon_social == "Juan Perez"
        assert client.nombre_comercial is None
        assert client.direccion is None
        assert client.ubigeo is None

    def test_full_client(self):
        """Full client with all optional fields."""
        client = Client(
            tipo_documento="6",
            numero_documento="20123456789",
            razon_social="EMPRESA CLIENTE SAC",
            nombre_comercial="Cliente Comercial",
            direccion="Av. Los Negocios 123, Miraflores",
            ubigeo="150122",
            distrito="Miraflores",
            provincia="Lima",
            departamento="Lima",
        )
        assert client.nombre_comercial == "Cliente Comercial"
        assert client.direccion == "Av. Los Negocios 123, Miraflores"
        assert client.ubigeo == "150122"

    def test_client_strips_whitespace(self):
        """Client should strip whitespace from string fields."""
        client = Client(
            tipo_documento="1",
            numero_documento="72345678",
            razon_social="  Juan Perez  ",
        )
        assert client.razon_social == "Juan Perez"
