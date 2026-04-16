"""Tests for Quotation model."""

from datetime import date

import pytest
from pydantic import ValidationError

from xfep.models.quotation import Quotation


def _make_quotation_data(**overrides):
    data = {
        "company_id": 1,
        "branch_id": 1,
        "serie": "COT1",
        "fecha_emision": date(2026, 2, 7),
        "dias_validez": 15,
        "moneda": "PEN",
        "tipo_operacion": "0101",
        "forma_pago_tipo": "Contado",
        "client": {
            "tipo_documento": "6",
            "numero_documento": "20512345678",
            "razon_social": "EMPRESA CLIENTE S.A.C.",
            "direccion": "Av. Arequipa 1234, Lima",
        },
        "detalles": [
            {
                "codigo": "PROD001",
                "descripcion": "Laptop HP ProBook 450 G8",
                "unidad": "NIU",
                "cantidad": 2,
                "mto_precio_unitario": 2500,
                "porcentaje_igv": 18,
                "tip_afe_igv": "10",
            }
        ],
    }
    data.update(overrides)
    return data


class TestQuotation:
    def test_valid_quotation(self):
        q = Quotation(**_make_quotation_data())
        assert q.serie == "COT1"
        assert q.dias_validez == 15

    def test_wrong_serie_prefix_rejected(self):
        with pytest.raises(ValidationError, match="must start with 'COT'"):
            Quotation(**_make_quotation_data(serie="F001"))

    def test_dias_validez_must_be_positive(self):
        with pytest.raises(ValidationError):
            Quotation(**_make_quotation_data(dias_validez=0))

    def test_condiciones_optional(self):
        q = Quotation(**_make_quotation_data(condiciones="Precios no incluyen flete"))
        assert q.condiciones == "Precios no incluyen flete"

    def test_condiciones_default_none(self):
        q = Quotation(**_make_quotation_data())
        assert q.condiciones is None

    def test_from_api_reference(self):
        """Full quotation matching the API reference example."""
        q = Quotation(
            company_id=1,
            branch_id=1,
            serie="COT1",
            fecha_emision="2026-02-07",
            dias_validez=15,
            moneda="PEN",
            tipo_operacion="0101",
            forma_pago_tipo="Contado",
            client={
                "tipo_documento": "6",
                "numero_documento": "20512345678",
                "razon_social": "EMPRESA CLIENTE S.A.C.",
                "direccion": "Av. Arequipa 1234, Lima",
            },
            detalles=[
                {
                    "codigo": "PROD001",
                    "descripcion": "Laptop HP ProBook 450 G8",
                    "unidad": "NIU",
                    "cantidad": 2,
                    "mto_precio_unitario": 2500,
                    "tip_afe_igv": "10",
                    "porcentaje_igv": 18,
                }
            ],
            condiciones="Precios no incluyen flete",
            usuario_creacion="vendedor01",
        )
        assert q.dias_validez == 15
        assert len(q.detalles) == 1
