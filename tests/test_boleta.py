"""Tests for Boleta model."""

from datetime import date

import pytest
from pydantic import ValidationError

from xfep.models.boleta import Boleta


def _make_boleta_data(**overrides):
    data = {
        "company_id": 1,
        "branch_id": 1,
        "serie": "B001",
        "fecha_emision": date(2026, 2, 17),
        "moneda": "PEN",
        "tipo_operacion": "0101",
        "forma_pago_tipo": "Contado",
        "client": {
            "tipo_documento": "1",
            "numero_documento": "67766554",
            "razon_social": "María Elena García Sánchez",
        },
        "detalles": [
            {
                "codigo": "LAPTOP001",
                "descripcion": "Laptop HP Pavilion",
                "unidad": "NIU",
                "cantidad": 1,
                "mto_precio_unitario": 12,
                "porcentaje_igv": 18,
                "tip_afe_igv": "10",
            }
        ],
    }
    data.update(overrides)
    return data


class TestBoleta:
    def test_valid_boleta(self):
        b = Boleta(**_make_boleta_data())
        assert b.serie == "B001"

    def test_defaults_to_resumen_diario(self):
        """Boleta without metodo_envio defaults to resumen_diario."""
        b = Boleta(**_make_boleta_data())
        assert b.metodo_envio == "resumen_diario"

    def test_metodo_envio_directo(self):
        b = Boleta(**_make_boleta_data(metodo_envio="directo"))
        assert b.metodo_envio == "directo"

    def test_wrong_serie_prefix_rejected(self):
        with pytest.raises(ValidationError, match="must start with 'B'"):
            Boleta(**_make_boleta_data(serie="F001"))

    def test_sin_documento_client(self):
        """Boleta allows client with tipo_documento='0' (sin documento)."""
        b = Boleta(
            **_make_boleta_data(
                client={
                    "tipo_documento": "0",
                    "numero_documento": "-",
                    "razon_social": "CLIENTE VARIOS",
                }
            )
        )
        assert b.client.tipo_documento == "0"

    def test_boleta_from_api_reference(self):
        """Full boleta matching the API reference example."""
        b = Boleta(
            company_id=1,
            branch_id=1,
            serie="B001",
            fecha_emision="2026-02-17",
            moneda="PEN",
            tipo_operacion="0101",
            metodo_envio="resumen_diario",
            forma_pago_tipo="Contado",
            client={
                "tipo_documento": "1",
                "numero_documento": "67766554",
                "razon_social": "María Elena García Sánchez",
            },
            detalles=[
                {
                    "codigo": "LAPTOP001",
                    "descripcion": "Laptop HP Pavilion 15.6\" Intel Core i5 8GB RAM",
                    "unidad": "NIU",
                    "cantidad": 1,
                    "mto_precio_unitario": 12,
                    "porcentaje_igv": 18,
                    "tip_afe_igv": "10",
                },
                {
                    "codigo": "LIBRO001",
                    "descripcion": "Libro de matemáticas educativo nivel secundaria",
                    "unidad": "NIU",
                    "cantidad": 2,
                    "mto_precio_unitario": 67,
                    "porcentaje_igv": 18,
                    "tip_afe_igv": "10",
                },
            ],
            usuario_creacion="vendedor01",
        )
        assert len(b.detalles) == 2
