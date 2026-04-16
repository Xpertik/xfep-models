"""Invoice (Factura) model."""

from typing import Self

from pydantic import model_validator

from .base import BaseDocument


class Invoice(BaseDocument):
    """Factura electrónica.

    Serie MUST start with 'F'. Client tipo_documento SHOULD be '6' (RUC).
    """

    @model_validator(mode="after")
    def _validate_serie_prefix(self) -> Self:
        if not self.serie.startswith("F"):
            raise ValueError(
                f"Invoice serie must start with 'F', got '{self.serie}'"
            )
        return self
