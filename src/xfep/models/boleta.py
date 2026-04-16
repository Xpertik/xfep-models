"""Boleta de Venta model."""

from typing import Self

from pydantic import model_validator

from .base import BaseDocument
from .enums import MetodoEnvio


class Boleta(BaseDocument):
    """Boleta de venta electrónica.

    Serie MUST start with 'B'. Has metodo_envio defaulting to resumen_diario.
    """

    metodo_envio: MetodoEnvio = MetodoEnvio.RESUMEN_DIARIO

    @model_validator(mode="after")
    def _validate_serie_prefix(self) -> Self:
        if not self.serie.startswith("B"):
            raise ValueError(
                f"Boleta serie must start with 'B', got '{self.serie}'"
            )
        return self
