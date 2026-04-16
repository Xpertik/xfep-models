"""Debit Note (Nota de Débito) model."""

from typing import Self

from pydantic import model_validator

from .base import NoteBase
from .detail import GuiaVinculada
from .enums import MotivoND, TipoDocumento


class DebitNote(NoteBase):
    """Nota de débito electrónica.

    Serie must start with 'FD' for facturas or 'BD' for boletas.
    cod_motivo uses MotivoND catalog.
    """

    cod_motivo: MotivoND  # type: ignore[assignment]
    guias: list[GuiaVinculada] | None = None

    @model_validator(mode="after")
    def _validate_serie_matches_affected(self) -> Self:
        prefix_map = {
            TipoDocumento.FACTURA: "FD",
            TipoDocumento.BOLETA: "BD",
        }
        expected = prefix_map.get(self.tipo_doc_afectado)
        if expected and not self.serie.startswith(expected):
            raise ValueError(
                f"DebitNote for {self.tipo_doc_afectado.name} must have serie "
                f"starting with '{expected}', got '{self.serie}'"
            )
        return self
