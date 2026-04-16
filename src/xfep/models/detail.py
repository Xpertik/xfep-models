"""Detail models for CPE and internal documents."""

from decimal import Decimal
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .enums import TipoAfectacionIGV, TipoDocumento, UnidadMedida


class Detalle(BaseModel):
    """Detalle de un CPE (Factura, Boleta, NC, ND).

    Exactly one of mto_precio_unitario or mto_valor_unitario must be provided.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    codigo: str | None = None
    descripcion: str
    unidad: UnidadMedida
    cantidad: Decimal = Field(gt=0)
    mto_precio_unitario: Decimal | None = None
    mto_valor_unitario: Decimal | None = None
    porcentaje_igv: Decimal
    tip_afe_igv: TipoAfectacionIGV
    descuento: Decimal | None = None
    isc: Decimal | None = None
    icbper: Decimal | None = None

    @model_validator(mode="after")
    def _exactly_one_price(self) -> Self:
        has_precio = self.mto_precio_unitario is not None
        has_valor = self.mto_valor_unitario is not None
        if has_precio == has_valor:
            raise ValueError(
                "Provide exactly one of mto_precio_unitario or mto_valor_unitario"
            )
        return self


class DetalleSimple(BaseModel):
    """Detalle simplificado para Nota de Venta y Cotización (sin IGV)."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    codigo: str | None = None
    descripcion: str
    unidad: UnidadMedida
    cantidad: Decimal = Field(gt=0)
    precio_unitario: Decimal


class GuiaVinculada(BaseModel):
    """Guía de remisión vinculada a un documento."""

    model_config = ConfigDict(populate_by_name=True)

    tipo_doc: TipoDocumento = TipoDocumento.GUIA_REMISION
    nro_doc: str


class VoidedDetail(BaseModel):
    """Detalle de un documento dentro de una Comunicación de Baja."""

    model_config = ConfigDict(populate_by_name=True)

    tipo_documento: TipoDocumento
    serie: str
    correlativo: str
    motivo_especifico: str
