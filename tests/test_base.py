"""Tests for BaseDocument, BaseSaleDocument, and NoteBase."""

from datetime import date

import pytest
from pydantic import ValidationError

from xfep.models.base import BaseDocument


def _make_base_data(**overrides):
    """Helper to create valid BaseDocument data."""
    data = {
        "company_id": 1,
        "branch_id": 1,
        "serie": "F001",
        "fecha_emision": date(2026, 2, 10),
        "client": {
            "tipo_documento": "6",
            "numero_documento": "20123456789",
            "razon_social": "EMPRESA SAC",
        },
        "detalles": [
            {
                "descripcion": "Producto",
                "unidad": "NIU",
                "cantidad": 1,
                "mto_precio_unitario": 100,
                "porcentaje_igv": 18,
                "tip_afe_igv": "10",
            }
        ],
    }
    data.update(overrides)
    return data


class TestBaseDocument:
    def test_valid_base(self):
        doc = BaseDocument(**_make_base_data())
        assert doc.company_id == 1
        assert doc.moneda == "PEN"
        assert doc.forma_pago_tipo == "Contado"

    def test_empty_detalles_rejected(self):
        """Document with empty detalles must be rejected."""
        with pytest.raises(ValidationError):
            BaseDocument(**_make_base_data(detalles=[]))

    def test_credit_without_cuotas_rejected(self):
        """Credit payment without cuotas must be rejected."""
        with pytest.raises(ValidationError, match="Credito requires"):
            BaseDocument(**_make_base_data(forma_pago_tipo="Credito"))

    def test_credit_with_cuotas_valid(self):
        doc = BaseDocument(
            **_make_base_data(
                forma_pago_tipo="Credito",
                forma_pago_cuotas=[
                    {"monto": 50, "fecha_pago": "2026-03-10"},
                ],
            )
        )
        assert len(doc.forma_pago_cuotas) == 1

    def test_contado_without_cuotas_valid(self):
        doc = BaseDocument(**_make_base_data(forma_pago_tipo="Contado"))
        assert doc.forma_pago_cuotas is None

    def test_contado_is_default(self):
        doc = BaseDocument(**_make_base_data())
        assert doc.forma_pago_tipo == "Contado"
