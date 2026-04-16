"""Tests for DebitNote model."""

from datetime import date

import pytest
from pydantic import ValidationError

from xfep.models.debit_note import DebitNote


def _make_nd_data(**overrides):
    data = {
        "company_id": 1,
        "branch_id": 1,
        "serie": "FD01",
        "fecha_emision": date(2026, 2, 7),
        "moneda": "PEN",
        "tipo_operacion": "0101",
        "forma_pago_tipo": "Contado",
        "tipo_doc_afectado": "01",
        "num_doc_afectado": "F001-000004",
        "cod_motivo": "02",
        "des_motivo": "AUMENTO EN EL VALOR",
        "client": {
            "tipo_documento": "6",
            "numero_documento": "20123456789",
            "razon_social": "EMPRESA DE PRUEBA SAC",
        },
        "detalles": [
            {
                "codigo": "C023",
                "descripcion": "AUMENTO POR CONCEPTO ADICIONAL",
                "unidad": "NIU",
                "cantidad": 2,
                "mto_precio_unitario": 30,
                "porcentaje_igv": 18,
                "tip_afe_igv": "10",
            }
        ],
    }
    data.update(overrides)
    return data


class TestDebitNote:
    def test_valid_nd_factura(self):
        """ND for factura with serie FD01 is valid."""
        nd = DebitNote(**_make_nd_data())
        assert nd.serie == "FD01"
        assert nd.cod_motivo == "02"

    def test_valid_nd_boleta(self):
        """ND for boleta with serie BD01 is valid."""
        nd = DebitNote(
            **_make_nd_data(serie="BD01", tipo_doc_afectado="03")
        )
        assert nd.serie == "BD01"

    def test_serie_mismatch_factura(self):
        """ND for factura with BD serie must be rejected."""
        with pytest.raises(ValidationError, match="FACTURA.*FD"):
            DebitNote(**_make_nd_data(serie="BD01", tipo_doc_afectado="01"))

    def test_serie_mismatch_boleta(self):
        """ND for boleta with FD serie must be rejected."""
        with pytest.raises(ValidationError, match="BOLETA.*BD"):
            DebitNote(**_make_nd_data(serie="FD01", tipo_doc_afectado="03"))

    def test_from_api_reference(self):
        """ND matching API reference example."""
        nd = DebitNote(
            company_id=1,
            branch_id=1,
            serie="FD01",
            fecha_emision="2026-02-07",
            moneda="PEN",
            tipo_operacion="0101",
            forma_pago_tipo="Contado",
            tipo_doc_afectado="01",
            num_doc_afectado="F001-000004",
            cod_motivo="02",
            des_motivo="AUMENTO EN EL VALOR",
            client={
                "tipo_documento": "6",
                "numero_documento": "20123456789",
                "razon_social": "EMPRESA DE PRUEBA SAC",
                "direccion": "AV. EJEMPLO 123",
                "ubigeo": "150101",
                "distrito": "LIMA",
                "provincia": "LIMA",
                "departamento": "LIMA",
            },
            detalles=[
                {
                    "codigo": "C023",
                    "descripcion": "AUMENTO POR CONCEPTO ADICIONAL",
                    "unidad": "NIU",
                    "cantidad": 2,
                    "mto_precio_unitario": 30,
                    "porcentaje_igv": 18,
                    "tip_afe_igv": "10",
                }
            ],
        )
        assert nd.des_motivo == "AUMENTO EN EL VALOR"
