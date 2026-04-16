"""Client model for electronic invoicing."""

from pydantic import BaseModel, ConfigDict

from .enums import TipoDocIdentidad


class Client(BaseModel):
    """Datos del cliente/receptor del comprobante."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    tipo_documento: TipoDocIdentidad
    numero_documento: str
    razon_social: str
    nombre_comercial: str | None = None
    direccion: str | None = None
    ubigeo: str | None = None
    distrito: str | None = None
    provincia: str | None = None
    departamento: str | None = None
