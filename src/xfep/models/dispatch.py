"""Dispatch Guide (Guía de Remisión Electrónica — GRE) model."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from .client import Client
from .enums import UnidadMedida


class Conductor(BaseModel):
    """Datos del conductor."""

    model_config = ConfigDict(populate_by_name=True)

    tipo_documento: str
    numero_documento: str
    nombres: str
    apellidos: str
    licencia: str | None = None


class Vehiculo(BaseModel):
    """Datos del vehículo de transporte."""

    model_config = ConfigDict(populate_by_name=True)

    placa: str
    marca: str | None = None
    certificado_inscripcion: str | None = None


class DireccionGRE(BaseModel):
    """Dirección para punto de partida/llegada."""

    model_config = ConfigDict(populate_by_name=True)

    ubigeo: str
    direccion: str
    distrito: str | None = None
    provincia: str | None = None
    departamento: str | None = None


class DetalleGRE(BaseModel):
    """Detalle de un ítem en la guía de remisión."""

    model_config = ConfigDict(populate_by_name=True)

    codigo: str | None = None
    descripcion: str
    unidad: UnidadMedida = UnidadMedida.UNIDAD
    cantidad: Decimal = Field(gt=0)


class DispatchGuide(BaseModel):
    """Guía de remisión electrónica (GRE).

    Standalone model — does NOT extend BaseDocument (structurally unique).
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    company_id: int
    branch_id: int
    serie: str
    fecha_emision: date
    motivo_traslado: str
    modalidad_transporte: str
    peso_total: Decimal = Field(gt=0)
    unidad_peso: UnidadMedida = UnidadMedida.KILOGRAMO
    punto_partida: DireccionGRE
    punto_llegada: DireccionGRE
    destinatario: Client
    transportista: Client | None = None
    vehiculo: Vehiculo | None = None
    conductor: Conductor | None = None
    detalles: list[DetalleGRE] = Field(min_length=1)
    observaciones: str | None = None
    usuario_creacion: str | None = None
