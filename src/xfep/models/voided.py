"""Voided Document (Comunicación de Baja) model."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from .detail import VoidedDetail


class VoidedDocument(BaseModel):
    """Comunicación de baja.

    Standalone model — does NOT extend BaseDocument.
    Used to void (anular) previously issued documents within 7 days.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    company_id: int
    branch_id: int
    fecha_referencia: date
    motivo_baja: str
    detalles: list[VoidedDetail] = Field(min_length=1)
    usuario_creacion: str | None = None
