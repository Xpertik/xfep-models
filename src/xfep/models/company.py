"""Company and Branch models."""

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Company(BaseModel):
    """Empresa emisora de comprobantes electrónicos."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    ruc: str = Field(min_length=11, max_length=11)
    razon_social: str
    nombre_comercial: str | None = None
    direccion: str | None = None
    ubigeo: str | None = None
    distrito: str | None = None
    provincia: str | None = None
    departamento: str | None = None
    email: str | None = None
    telefono: str | None = None
    usuario_sol: str | None = None
    clave_sol: str | None = None
    modo_produccion: bool = False
    activo: bool = True

    @model_validator(mode="after")
    def _validate_ruc_prefix(self) -> Self:
        if self.ruc[:2] not in ("10", "20"):
            raise ValueError(
                f"RUC must start with '10' or '20', got '{self.ruc[:2]}'"
            )
        return self


class Branch(BaseModel):
    """Sucursal / establecimiento anexo."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    company_id: int
    codigo: str = Field(min_length=4, max_length=4)
    nombre: str
    direccion: str | None = None
    ubigeo: str | None = None
    distrito: str | None = None
    provincia: str | None = None
    departamento: str | None = None
    telefono: str | None = None
    email: str | None = None
