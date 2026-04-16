"""Tests for payment models."""

from datetime import date

import pytest
from pydantic import ValidationError

from xfep.models.payment import Anticipo, CuotaPago, Detraccion, Percepcion


class TestCuotaPago:
    def test_valid_cuota(self):
        cuota = CuotaPago(monto=500.00, fecha_pago=date(2026, 3, 15))
        assert cuota.monto == 500.00
        assert cuota.fecha_pago == date(2026, 3, 15)

    def test_zero_monto_rejected(self):
        with pytest.raises(ValidationError):
            CuotaPago(monto=0, fecha_pago=date(2026, 3, 15))

    def test_negative_monto_rejected(self):
        with pytest.raises(ValidationError):
            CuotaPago(monto=-100, fecha_pago=date(2026, 3, 15))


class TestDetraccion:
    def test_valid_detraccion(self):
        d = Detraccion(
            codigo="022",
            porcentaje=12,
            monto=120.00,
            cuenta_bancaria="00-123-456789",
        )
        assert d.codigo == "022"
        assert d.porcentaje == 12


class TestPercepcion:
    def test_valid_percepcion(self):
        p = Percepcion(
            codigo="01",
            porcentaje=2,
            monto=20.00,
            monto_total=1020.00,
        )
        assert p.monto_total == 1020.00


class TestAnticipo:
    def test_valid_anticipo(self):
        a = Anticipo(tipo_doc="02", nro_doc="F001-000001", monto=500)
        assert a.monto == 500
