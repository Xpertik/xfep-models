"""Tests for response models — round-trip JSON -> model -> JSON."""

from datetime import date

from xfep.models.responses import DocumentResponse, SummaryResponse, VoidedResponse


class TestDocumentResponse:
    def test_from_api_reference_invoice(self):
        """Parse invoice response from API reference."""
        data = {
            "id": 150,
            "serie": "F001",
            "correlativo": "25",
            "tipo_documento": "01",
            "fecha_emision": "2026-02-10",
            "total_gravadas": 237.9,
            "total_igv": 42.78,
            "total_venta": 280.68,
            "estado": "GENERADO",
            "estado_sunat": "PENDIENTE",
            "xml_generado": True,
        }
        r = DocumentResponse(**data)
        assert r.id == 150
        assert r.serie == "F001"
        from decimal import Decimal
        assert r.total_venta == Decimal("280.68")
        assert r.estado == "GENERADO"
        assert r.estado_sunat == "PENDIENTE"
        assert r.xml_generado is True

    def test_from_api_reference_boleta(self):
        """Parse boleta response from API reference."""
        data = {
            "id": 305,
            "serie": "B001",
            "correlativo": "48",
            "tipo_documento": "03",
            "fecha_emision": "2026-02-17",
            "total_gravadas": 123.73,
            "total_igv": 22.27,
            "total_venta": 146,
            "estado": "GENERADO",
            "estado_sunat": "PENDIENTE",
            "xml_generado": True,
        }
        r = DocumentResponse(**data)
        assert r.tipo_documento == "03"

    def test_round_trip(self):
        """Round-trip: dict -> model -> dict."""
        data = {
            "id": 85,
            "serie": "FF01",
            "correlativo": "12",
            "tipo_documento": "07",
            "fecha_emision": "2026-02-07",
            "total_gravadas": 100,
            "total_igv": 18,
            "total_venta": 118,
            "estado": "GENERADO",
            "estado_sunat": "PENDIENTE",
            "xml_generado": True,
        }
        r = DocumentResponse(**data)
        dumped = r.model_dump()
        assert dumped["id"] == 85
        assert dumped["serie"] == "FF01"

    def test_optional_totals(self):
        """Optional totals default to None."""
        r = DocumentResponse(
            id=1,
            serie="F001",
            correlativo="1",
            tipo_documento="01",
            fecha_emision=date(2026, 1, 1),
            total_gravadas=100,
            total_igv=18,
            total_venta=118,
            estado="GENERADO",
            estado_sunat="PENDIENTE",
            xml_generado=True,
        )
        assert r.total_exoneradas is None
        assert r.total_inafectas is None
        assert r.total_isc is None
        assert r.total_icbper is None


class TestVoidedResponse:
    def test_from_api_reference(self):
        data = {
            "id": 15,
            "identificador": "RA-20260130-001",
            "fecha_generacion": "2026-01-30",
            "fecha_referencia": "2026-01-30",
            "motivo_baja": "ERROR EN CÁLCULO DE IGV",
            "cantidad_documentos": 1,
            "estado": "GENERADO",
            "estado_sunat": "PENDIENTE",
        }
        r = VoidedResponse(**data)
        assert r.identificador == "RA-20260130-001"
        assert r.cantidad_documentos == 1

    def test_round_trip(self):
        r = VoidedResponse(
            id=15,
            identificador="RA-20260130-001",
            fecha_generacion=date(2026, 1, 30),
            fecha_referencia=date(2026, 1, 30),
            motivo_baja="ERROR",
            cantidad_documentos=1,
            estado="GENERADO",
            estado_sunat="PENDIENTE",
        )
        dumped = r.model_dump()
        assert dumped["identificador"] == "RA-20260130-001"


class TestSummaryResponse:
    def test_valid(self):
        r = SummaryResponse(
            id=1,
            identificador="RC-20260217-001",
            fecha_resumen=date(2026, 2, 17),
            cantidad_documentos=5,
            estado="GENERADO",
            estado_sunat="PENDIENTE",
        )
        assert r.identificador == "RC-20260217-001"
        assert r.cantidad_documentos == 5

    def test_round_trip(self):
        r = SummaryResponse(
            id=1,
            identificador="RC-20260217-001",
            fecha_resumen=date(2026, 2, 17),
            cantidad_documentos=5,
            estado="GENERADO",
            estado_sunat="PENDIENTE",
        )
        dumped = r.model_dump()
        r2 = SummaryResponse(**dumped)
        assert r2.id == r.id
