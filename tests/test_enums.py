"""Tests for SUNAT catalog enums."""

import pytest

from xfep.models.enums import (
    EstadoDocumento,
    EstadoSunat,
    FormaPago,
    MetodoEnvio,
    Moneda,
    MotivoNC,
    MotivoND,
    TipoAfectacionIGV,
    TipoDocIdentidad,
    TipoDocumento,
    TipoOperacion,
    UnidadMedida,
)


class TestTipoDocumento:
    def test_factura_value(self):
        assert TipoDocumento.FACTURA == "01"
        assert TipoDocumento.FACTURA.value == "01"

    def test_boleta_value(self):
        assert TipoDocumento.BOLETA == "03"

    def test_nota_credito_value(self):
        assert TipoDocumento.NOTA_CREDITO == "07"

    def test_nota_debito_value(self):
        assert TipoDocumento.NOTA_DEBITO == "08"

    def test_guia_remision_value(self):
        assert TipoDocumento.GUIA_REMISION == "09"

    def test_all_members_are_strings(self):
        for member in TipoDocumento:
            assert isinstance(member.value, str)


class TestTipoDocIdentidad:
    def test_sin_documento(self):
        assert TipoDocIdentidad.SIN_DOCUMENTO == "0"

    def test_dni(self):
        assert TipoDocIdentidad.DNI == "1"

    def test_ruc(self):
        assert TipoDocIdentidad.RUC == "6"

    def test_pasaporte(self):
        assert TipoDocIdentidad.PASAPORTE == "7"


class TestTipoAfectacionIGV:
    def test_gravado(self):
        assert TipoAfectacionIGV.GRAVADO == "10"

    def test_exonerado(self):
        assert TipoAfectacionIGV.EXONERADO == "20"

    def test_inafecto(self):
        assert TipoAfectacionIGV.INAFECTO == "30"

    def test_ivap(self):
        assert TipoAfectacionIGV.IVAP == "17"


class TestMoneda:
    def test_pen(self):
        assert Moneda.PEN == "PEN"

    def test_usd(self):
        assert Moneda.USD == "USD"

    def test_invalid_currency_rejected(self):
        with pytest.raises(ValueError):
            Moneda("EUR")


class TestTipoOperacion:
    def test_venta_interna(self):
        assert TipoOperacion.VENTA_INTERNA == "0101"

    def test_exportacion_bienes(self):
        assert TipoOperacion.EXPORTACION_BIENES == "0200"


class TestUnidadMedida:
    def test_unidad(self):
        assert UnidadMedida.UNIDAD == "NIU"

    def test_servicio(self):
        assert UnidadMedida.SERVICIO == "ZZ"

    def test_kilogramo(self):
        assert UnidadMedida.KILOGRAMO == "KGM"


class TestMotivoNC:
    def test_anulacion(self):
        assert MotivoNC.ANULACION == "01"

    def test_devolucion_item(self):
        assert MotivoNC.DEVOLUCION_ITEM == "07"

    def test_member_count(self):
        assert len(MotivoNC) == 12


class TestMotivoND:
    def test_intereses_mora(self):
        assert MotivoND.INTERESES_MORA == "01"

    def test_aumento_valor(self):
        assert MotivoND.AUMENTO_VALOR == "02"


class TestFormaPago:
    def test_contado(self):
        assert FormaPago.CONTADO == "Contado"

    def test_credito(self):
        assert FormaPago.CREDITO == "Credito"


class TestMetodoEnvio:
    def test_resumen_diario(self):
        assert MetodoEnvio.RESUMEN_DIARIO == "resumen_diario"

    def test_directo(self):
        assert MetodoEnvio.DIRECTO == "directo"


class TestEstados:
    def test_estado_documento_generado(self):
        assert EstadoDocumento.GENERADO == "GENERADO"

    def test_estado_sunat_pendiente(self):
        assert EstadoSunat.PENDIENTE == "PENDIENTE"

    def test_estado_sunat_aceptado(self):
        assert EstadoSunat.ACEPTADO == "ACEPTADO"
