"""Quotation (Cotización) model."""

from typing import Self

from pydantic import Field, model_validator

from .base import BaseDocument


class Quotation(BaseDocument):
    """Cotización (no se envía a SUNAT).

    Serie MUST start with 'COT'.
    """

    dias_validez: int = Field(gt=0)
    condiciones: str | None = None

    @model_validator(mode="after")
    def _validate_serie_prefix(self) -> Self:
        if not self.serie.startswith("COT"):
            raise ValueError(
                f"Quotation serie must start with 'COT', got '{self.serie}'"
            )
        return self
