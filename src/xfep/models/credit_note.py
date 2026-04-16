"""Credit Note (Nota de Crédito) model."""

from typing import Self

from pydantic import model_validator

from .base import NoteBase
from .detail import GuiaVinculada
from .enums import MotivoNC, TipoDocumento


class CreditNote(NoteBase):
    """Nota de crédito electrónica.

    Serie must start with 'FF' for facturas or 'BB' for boletas.
    cod_motivo uses MotivoNC catalog.
    """

    cod_motivo: MotivoNC  # type: ignore[assignment]
    guias: list[GuiaVinculada] | None = None

    @model_validator(mode="after")
    def _validate_serie_matches_affected(self) -> Self:
        prefix_map = {
            TipoDocumento.FACTURA: "FF",
            TipoDocumento.BOLETA: "BB",
        }
        expected = prefix_map.get(self.tipo_doc_afectado)
        if expected and not self.serie.startswith(expected):
            raise ValueError(
                f"CreditNote for {self.tipo_doc_afectado.name} must have serie "
                f"starting with '{expected}', got '{self.serie}'"
            )
        return self
