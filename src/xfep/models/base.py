"""Base document models for CPE and internal documents."""

from datetime import date
from decimal import Decimal
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .client import Client
from .detail import Detalle, DetalleSimple
from .enums import (
    FormaPago,
    Moneda,
    TipoDocumento,
    TipoOperacion,
)
from .payment import Anticipo, CuotaPago, Detraccion, Percepcion


class BaseDocument(BaseModel):
    """Base model for CPE documents (Factura, Boleta, NC, ND, Cotización).

    Contains all shared fields across CPE document types.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_default=True,
        populate_by_name=True,
    )

    company_id: int
    branch_id: int
    serie: str
    fecha_emision: date
    moneda: Moneda = Moneda.PEN
    tipo_operacion: TipoOperacion = TipoOperacion.VENTA_INTERNA
    forma_pago_tipo: FormaPago = FormaPago.CONTADO
    client: Client
    detalles: list[Detalle] = Field(min_length=1)
    forma_pago_cuotas: list[CuotaPago] | None = None
    descuento_global: Decimal | None = None
    detracciones: Detraccion | None = None
    percepciones: Percepcion | None = None
    anticipos: list[Anticipo] | None = None
    guia_remision: dict | None = None
    observaciones: str | None = None
    usuario_creacion: str | None = None

    @model_validator(mode="after")
    def _validate_credit_cuotas(self) -> Self:
        if self.forma_pago_tipo == FormaPago.CREDITO:
            if not self.forma_pago_cuotas:
                raise ValueError(
                    "Credito requires at least one CuotaPago in forma_pago_cuotas"
                )
        return self


class NoteBase(BaseDocument):
    """Base model for NC and ND documents.

    Adds affected document reference fields to BaseDocument.
    """

    tipo_doc_afectado: TipoDocumento
    num_doc_afectado: str
    cod_motivo: str
    des_motivo: str


class BaseSaleDocument(BaseModel):
    """Base model for internal sale documents (Nota de Venta).

    Uses DetalleSimple (no IGV fields).
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_default=True,
        populate_by_name=True,
    )

    company_id: int
    branch_id: int
    serie: str
    fecha_emision: date
    moneda: Moneda = Moneda.PEN
    client: Client
    detalles: list[DetalleSimple] = Field(min_length=1)
    observaciones: str | None = None
    usuario_creacion: str | None = None
