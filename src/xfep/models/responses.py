"""Response models for API responses."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from .enums import EstadoDocumento, EstadoSunat


class DocumentResponse(BaseModel):
    """Response for created CPE documents (Invoice, Boleta, NC, ND)."""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    serie: str
    correlativo: str
    tipo_documento: str
    fecha_emision: date
    total_gravadas: Decimal
    total_igv: Decimal
    total_venta: Decimal
    estado: EstadoDocumento
    estado_sunat: EstadoSunat
    xml_generado: bool
    total_exoneradas: Decimal | None = None
    total_inafectas: Decimal | None = None
    total_isc: Decimal | None = None
    total_icbper: Decimal | None = None


class VoidedResponse(BaseModel):
    """Response for voided document (Comunicación de Baja)."""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    identificador: str
    fecha_generacion: date
    fecha_referencia: date
    motivo_baja: str
    cantidad_documentos: int
    estado: EstadoDocumento
    estado_sunat: EstadoSunat


class SummaryResponse(BaseModel):
    """Response for daily summary (Resumen Diario)."""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    identificador: str
    fecha_resumen: date
    cantidad_documentos: int
    estado: EstadoDocumento
    estado_sunat: EstadoSunat
