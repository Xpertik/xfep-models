"""Sale Note (Nota de Venta) model."""

from typing import Self

from pydantic import model_validator

from .base import BaseSaleDocument


class SaleNote(BaseSaleDocument):
    """Nota de venta (no se envía a SUNAT).

    Serie MUST start with 'NV'. Uses DetalleSimple (no IGV fields).
    """

    @model_validator(mode="after")
    def _validate_serie_prefix(self) -> Self:
        if not self.serie.startswith("NV"):
            raise ValueError(
                f"SaleNote serie must start with 'NV', got '{self.serie}'"
            )
        return self
