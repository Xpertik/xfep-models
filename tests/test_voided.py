"""Tests for VoidedDocument model."""

from datetime import date

import pytest
from pydantic import ValidationError

from xfep.models.voided import VoidedDocument


class TestVoidedDocument:
    def test_valid_voided(self):
        """Valid VoidedDocument from API reference."""
        vd = VoidedDocument(
            company_id=1,
            branch_id=1,
            fecha_referencia=date(2026, 1, 30),
            motivo_baja="ERROR EN CÁLCULO DE IGV - DOCUMENTO NO ENTREGADO AL CLIENTE",
            detalles=[
                {
                    "tipo_documento": "01",
                    "serie": "F001",
                    "correlativo": "000023",
                    "motivo_especifico": "Error en aplicación de IGV por tipo de afectación incorrecta",
                }
            ],
            usuario_creacion="admin",
        )
        assert vd.fecha_referencia == date(2026, 1, 30)
        assert len(vd.detalles) == 1
        assert vd.detalles[0].tipo_documento == "01"

    def test_multiple_detalles(self):
        vd = VoidedDocument(
            company_id=1,
            branch_id=1,
            fecha_referencia=date(2026, 1, 30),
            motivo_baja="Error masivo",
            detalles=[
                {
                    "tipo_documento": "01",
                    "serie": "F001",
                    "correlativo": "000023",
                    "motivo_especifico": "Error 1",
                },
                {
                    "tipo_documento": "07",
                    "serie": "FF01",
                    "correlativo": "000005",
                    "motivo_especifico": "Error 2",
                },
            ],
        )
        assert len(vd.detalles) == 2

    def test_empty_detalles_rejected(self):
        with pytest.raises(ValidationError):
            VoidedDocument(
                company_id=1,
                branch_id=1,
                fecha_referencia=date(2026, 1, 30),
                motivo_baja="Error",
                detalles=[],
            )
