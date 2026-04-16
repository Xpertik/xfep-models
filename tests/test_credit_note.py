"""Tests for CreditNote model."""

from datetime import date

import pytest
from pydantic import ValidationError

from xfep.models.credit_note import CreditNote


def _make_nc_data(**overrides):
    data = {
        "company_id": 1,
        "branch_id": 1,
        "serie": "FF01",
        "fecha_emision": date(2026, 2, 7),
        "moneda": "PEN",
        "tipo_operacion": "0101",
        "forma_pago_tipo": "Contado",
        "tipo_doc_afectado": "01",
        "num_doc_afectado": "F001-000047",
        "cod_motivo": "07",
        "des_motivo": "DEVOLUCION POR ITEM",
        "client": {
            "tipo_documento": "6",
            "numero_documento": "20123456789",
            "razon_social": "EMPRESA DE PRUEBA SAC",
        },
        "detalles": [
            {
                "codigo": "C023",
                "descripcion": "PRODUCTO 1",
                "unidad": "NIU",
                "cantidad": 2,
                "mto_precio_unitario": 25,
                "porcentaje_igv": 18,
                "tip_afe_igv": "10",
            }
        ],
    }
    data.update(overrides)
    return data


class TestCreditNote:
    def test_valid_nc_factura(self):
        """NC for factura with serie FF01 is valid."""
        nc = CreditNote(**_make_nc_data())
        assert nc.serie == "FF01"
        assert nc.tipo_doc_afectado == "01"
        assert nc.cod_motivo == "07"

    def test_valid_nc_boleta(self):
        """NC for boleta with serie BB01 is valid."""
        nc = CreditNote(
            **_make_nc_data(
                serie="BB01",
                tipo_doc_afectado="03",
            )
        )
        assert nc.serie == "BB01"
        assert nc.tipo_doc_afectado == "03"

    def test_serie_mismatch_factura(self):
        """NC for factura with BB serie must be rejected."""
        with pytest.raises(ValidationError, match="FACTURA.*FF"):
            CreditNote(**_make_nc_data(serie="BB01", tipo_doc_afectado="01"))

    def test_serie_mismatch_boleta(self):
        """NC for boleta with FF serie must be rejected."""
        with pytest.raises(ValidationError, match="BOLETA.*BB"):
            CreditNote(**_make_nc_data(serie="FF01", tipo_doc_afectado="03"))

    def test_with_guias(self):
        """NC with guías vinculadas."""
        nc = CreditNote(
            **_make_nc_data(
                guias=[{"tipo_doc": "09", "nro_doc": "0001-213"}]
            )
        )
        assert len(nc.guias) == 1
        assert nc.guias[0].nro_doc == "0001-213"

    def test_from_api_reference(self):
        """NC matching API reference example."""
        nc = CreditNote(
            company_id=1,
            branch_id=1,
            serie="FF01",
            fecha_emision="2026-02-07",
            moneda="PEN",
            tipo_operacion="0101",
            forma_pago_tipo="Contado",
            tipo_doc_afectado="01",
            num_doc_afectado="F001-000047",
            cod_motivo="07",
            des_motivo="DEVOLUCION POR ITEM",
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
            guias=[{"tipo_doc": "09", "nro_doc": "0001-213"}],
            detalles=[
                {
                    "codigo": "C023",
                    "descripcion": "PRODUCTO 1",
                    "unidad": "NIU",
                    "cantidad": 2,
                    "mto_precio_unitario": 25,
                    "porcentaje_igv": 18,
                    "tip_afe_igv": "10",
                }
            ],
        )
        assert nc.des_motivo == "DEVOLUCION POR ITEM"
