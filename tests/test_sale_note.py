"""Tests for SaleNote model."""

from datetime import date

import pytest
from pydantic import ValidationError

from xfep.models.sale_note import SaleNote


def _make_nv_data(**overrides):
    data = {
        "company_id": 1,
        "branch_id": 1,
        "serie": "NV01",
        "fecha_emision": date(2026, 1, 30),
        "moneda": "PEN",
        "client": {
            "tipo_documento": "1",
            "numero_documento": "72345678",
            "razon_social": "Juan Perez Garcia",
        },
        "detalles": [
            {
                "codigo": "PROD001",
                "descripcion": "Laptop HP Pavilion",
                "unidad": "NIU",
                "cantidad": 1,
                "precio_unitario": 45,
            }
        ],
    }
    data.update(overrides)
    return data


class TestSaleNote:
    def test_valid_sale_note(self):
        nv = SaleNote(**_make_nv_data())
        assert nv.serie == "NV01"
        assert len(nv.detalles) == 1

    def test_wrong_serie_prefix_rejected(self):
        with pytest.raises(ValidationError, match="must start with 'NV'"):
            SaleNote(**_make_nv_data(serie="F001"))

    def test_detalle_simple_has_no_igv_fields(self):
        """DetalleSimple uses precio_unitario, not mto_precio_unitario."""
        nv = SaleNote(**_make_nv_data())
        assert hasattr(nv.detalles[0], "precio_unitario")
        assert not hasattr(nv.detalles[0], "tip_afe_igv")

    def test_from_api_reference(self):
        """Match the API reference NV example."""
        nv = SaleNote(
            company_id=1,
            branch_id=1,
            serie="NV01",
            fecha_emision="2026-01-30",
            moneda="PEN",
            client={
                "tipo_documento": "1",
                "numero_documento": "72345678",
                "razon_social": "Juan Perez Garcia",
                "direccion": "Av. Los Pinos 456, Lima",
            },
            detalles=[
                {
                    "codigo": "PROD001",
                    "descripcion": "Laptop HP Pavilion 15.6 pulgadas",
                    "unidad": "NIU",
                    "cantidad": 1,
                    "precio_unitario": 45,
                },
                {
                    "descripcion": "Garantía extendida 2 años",
                    "unidad": "ZZ",
                    "cantidad": 1,
                    "precio_unitario": 150,
                },
            ],
            observaciones="Cliente solicita factura posteriormente",
        )
        assert len(nv.detalles) == 2
        assert nv.detalles[1].codigo is None
        assert nv.observaciones == "Cliente solicita factura posteriormente"

    def test_empty_detalles_rejected(self):
        with pytest.raises(ValidationError):
            SaleNote(**_make_nv_data(detalles=[]))
