"""Payment-related models: installments, detractions, perceptions, advances."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CuotaPago(BaseModel):
    """Cuota de pago para ventas al crédito."""

    model_config = ConfigDict(populate_by_name=True)

    monto: Decimal = Field(gt=0)
    fecha_pago: date


class Detraccion(BaseModel):
    """Detracción SUNAT."""

    model_config = ConfigDict(populate_by_name=True)

    codigo: str
    porcentaje: Decimal
    monto: Decimal
    cuenta_bancaria: str | None = None


class Percepcion(BaseModel):
    """Percepción."""

    model_config = ConfigDict(populate_by_name=True)

    codigo: str
    porcentaje: Decimal
    monto: Decimal
    monto_total: Decimal


class Retencion(BaseModel):
    """Retención."""

    model_config = ConfigDict(populate_by_name=True)

    codigo: str
    porcentaje: Decimal
    monto: Decimal


class Anticipo(BaseModel):
    """Anticipo aplicado a un comprobante."""

    model_config = ConfigDict(populate_by_name=True)

    tipo_doc: str
    nro_doc: str
    monto: Decimal
