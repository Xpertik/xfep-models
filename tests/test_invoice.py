"""Tests for Invoice model."""

from datetime import date

import pytest
from pydantic import ValidationError

from xfep.models.invoice import Invoice


def _make_invoice_data(**overrides):
    """Helper to create valid invoice data."""
    data = {
        "company_id": 1,
        "branch_id": 1,
        "serie": "F001",
        "fecha_emision": date(2026, 2, 10),
        "moneda": "PEN",
        "tipo_operacion": "0101",
        "forma_pago_tipo": "Contado",
        "client": {
            "tipo_documento": "6",
            "numero_documento": "20123456789",
            "razon_social": "EMPRESA CLIENTE SAC",
        },
        "detalles": [
            {
                "codigo": "PROD001",
                "descripcion": "Laptop HP Pavilion",
                "unidad": "NIU",
                "cantidad": 4.678,
                "mto_precio_unitario": 60,
                "porcentaje_igv": 18,
                "tip_afe_igv": "10",
            }
        ],
    }
    data.update(overrides)
    return data


class TestInvoice:
    def test_valid_invoice(self):
        """Invoice with serie starting with 'F' is valid."""
        inv = Invoice(**_make_invoice_data())
        assert inv.serie == "F001"
        assert inv.client.tipo_documento == "6"
        assert len(inv.detalles) == 1

    def test_wrong_serie_prefix_rejected(self):
        """Invoice with serie starting with 'B' must be rejected."""
        with pytest.raises(ValidationError, match="must start with 'F'"):
            Invoice(**_make_invoice_data(serie="B001"))

    def test_empty_detalles_rejected(self):
        """Invoice with empty detalles must be rejected."""
        with pytest.raises(ValidationError):
            Invoice(**_make_invoice_data(detalles=[]))

    def test_credit_requires_cuotas(self):
        """Invoice with Credito must have cuotas."""
        with pytest.raises(ValidationError, match="Credito requires"):
            Invoice(**_make_invoice_data(forma_pago_tipo="Credito"))

    def test_credit_with_cuotas_valid(self):
        """Invoice with Credito and cuotas is valid."""
        inv = Invoice(
            **_make_invoice_data(
                forma_pago_tipo="Credito",
                forma_pago_cuotas=[
                    {"monto": 100, "fecha_pago": "2026-03-10"},
                    {"monto": 100, "fecha_pago": "2026-04-10"},
                ],
            )
        )
        assert len(inv.forma_pago_cuotas) == 2

    def test_contado_without_cuotas_valid(self):
        """Invoice with Contado and no cuotas is valid."""
        inv = Invoice(**_make_invoice_data())
        assert inv.forma_pago_tipo == "Contado"
        assert inv.forma_pago_cuotas is None

    def test_defaults(self):
        """Invoice defaults: moneda=PEN, tipo_operacion=0101, forma_pago=Contado."""
        inv = Invoice(**_make_invoice_data())
        assert inv.moneda == "PEN"
        assert inv.tipo_operacion == "0101"
        assert inv.forma_pago_tipo == "Contado"

    def test_full_invoice_from_api_reference(self):
        """Test with data matching the API reference example."""
        inv = Invoice(
            company_id=1,
            branch_id=1,
            serie="F001",
            fecha_emision="2026-02-10",
            moneda="PEN",
            tipo_operacion="0101",
            forma_pago_tipo="Contado",
            client={
                "tipo_documento": "6",
                "numero_documento": "20123456789",
                "razon_social": "EMPRESA CLIENTE SAC",
                "nombre_comercial": "Cliente Comercial",
                "direccion": "Av. Los Negocios 123, Miraflores",
            },
            detalles=[
                {
                    "codigo": "86GUGUYTT7",
                    "descripcion": "Laptop HP Pavilion 15.6",
                    "unidad": "KGM",
                    "cantidad": 4.678,
                    "mto_precio_unitario": 60,
                    "porcentaje_igv": 18,
                    "tip_afe_igv": "10",
                }
            ],
            usuario_creacion="admin",
        )
        assert inv.usuario_creacion == "admin"
        assert inv.client.nombre_comercial == "Cliente Comercial"
