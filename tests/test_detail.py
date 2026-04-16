"""Tests for Detalle and DetalleSimple models."""

import pytest
from pydantic import ValidationError

from xfep.models.detail import Detalle, DetalleSimple, GuiaVinculada, VoidedDetail


class TestDetalle:
    def test_with_precio_unitario(self):
        """Valid detalle with mto_precio_unitario only."""
        d = Detalle(
            codigo="LAPTOP001",
            descripcion="Laptop HP Pavilion",
            unidad="NIU",
            cantidad=1,
            mto_precio_unitario=12,
            porcentaje_igv=18,
            tip_afe_igv="10",
        )
        assert d.mto_precio_unitario == 12
        assert d.mto_valor_unitario is None

    def test_with_valor_unitario(self):
        """Valid detalle with mto_valor_unitario only."""
        d = Detalle(
            descripcion="Servicio consultoría",
            unidad="ZZ",
            cantidad=1,
            mto_valor_unitario=84.75,
            porcentaje_igv=18,
            tip_afe_igv="10",
        )
        assert d.mto_valor_unitario == 84.75
        assert d.mto_precio_unitario is None

    def test_both_prices_rejected(self):
        """Both mto_precio_unitario AND mto_valor_unitario must be rejected."""
        with pytest.raises(ValidationError, match="exactly one"):
            Detalle(
                descripcion="Producto",
                unidad="NIU",
                cantidad=1,
                mto_precio_unitario=100,
                mto_valor_unitario=84.75,
                porcentaje_igv=18,
                tip_afe_igv="10",
            )

    def test_neither_price_rejected(self):
        """Neither mto_precio_unitario nor mto_valor_unitario must be rejected."""
        with pytest.raises(ValidationError, match="exactly one"):
            Detalle(
                descripcion="Producto",
                unidad="NIU",
                cantidad=1,
                porcentaje_igv=18,
                tip_afe_igv="10",
            )

    def test_zero_cantidad_rejected(self):
        """Cantidad must be > 0."""
        with pytest.raises(ValidationError):
            Detalle(
                descripcion="Producto",
                unidad="NIU",
                cantidad=0,
                mto_precio_unitario=10,
                porcentaje_igv=18,
                tip_afe_igv="10",
            )

    def test_optional_fields(self):
        """Optional fields: descuento, isc, icbper."""
        from decimal import Decimal

        d = Detalle(
            descripcion="Bolsa plástica",
            unidad="NIU",
            cantidad=5,
            mto_precio_unitario=0.50,
            porcentaje_igv=18,
            tip_afe_igv="10",
            icbper=0.40,
        )
        assert d.icbper == Decimal("0.4")
        assert d.descuento is None
        assert d.isc is None


class TestDetalleSimple:
    def test_valid_simple(self):
        """Valid DetalleSimple for sale note."""
        d = DetalleSimple(
            codigo="PROD001",
            descripcion="Laptop HP Pavilion",
            unidad="NIU",
            cantidad=1,
            precio_unitario=45,
        )
        assert d.precio_unitario == 45
        assert d.codigo == "PROD001"

    def test_without_codigo(self):
        """DetalleSimple without codigo is valid."""
        d = DetalleSimple(
            descripcion="Garantía extendida",
            unidad="ZZ",
            cantidad=1,
            precio_unitario=150,
        )
        assert d.codigo is None


class TestGuiaVinculada:
    def test_guia_vinculada(self):
        g = GuiaVinculada(tipo_doc="09", nro_doc="0001-213")
        assert g.tipo_doc == "09"
        assert g.nro_doc == "0001-213"


class TestVoidedDetail:
    def test_voided_detail(self):
        vd = VoidedDetail(
            tipo_documento="01",
            serie="F001",
            correlativo="000023",
            motivo_especifico="Error en IGV",
        )
        assert vd.tipo_documento == "01"
        assert vd.serie == "F001"
