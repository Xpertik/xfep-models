"""xfep-models — Pydantic v2 data models for Peruvian electronic invoicing.

Public API re-exports all models and enums for convenient access:

    from xfep.models import Invoice, Boleta, Client, Detalle
"""

# Enums
from .enums import (
    EstadoDocumento,
    EstadoSunat,
    FormaPago,
    MetodoEnvio,
    Moneda,
    MotivoNC,
    MotivoND,
    TipoAfectacionIGV,
    TipoDocIdentidad,
    TipoDocumento,
    TipoOperacion,
    UnidadMedida,
)

# Entities
from .client import Client
from .company import Branch, Company
from .detail import DetalleSimple, Detalle, GuiaVinculada, VoidedDetail
from .payment import Anticipo, CuotaPago, Detraccion, Percepcion, Retencion

# Base
from .base import BaseDocument, BaseSaleDocument, NoteBase

# Documents
from .invoice import Invoice
from .boleta import Boleta
from .credit_note import CreditNote
from .debit_note import DebitNote
from .quotation import Quotation
from .sale_note import SaleNote

# Standalone documents
from .voided import VoidedDocument
from .summary import DailySummary
from .dispatch import (
    Conductor,
    DetalleGRE,
    DireccionGRE,
    DispatchGuide,
    Vehiculo,
)

# Webhook
from .webhook import Webhook

# Responses
from .responses import DocumentResponse, SummaryResponse, VoidedResponse

__all__ = [
    # Enums
    "TipoDocumento",
    "TipoDocIdentidad",
    "TipoAfectacionIGV",
    "Moneda",
    "TipoOperacion",
    "UnidadMedida",
    "MotivoNC",
    "MotivoND",
    "FormaPago",
    "MetodoEnvio",
    "EstadoDocumento",
    "EstadoSunat",
    # Entities
    "Client",
    "Detalle",
    "DetalleSimple",
    "GuiaVinculada",
    "VoidedDetail",
    "CuotaPago",
    "Detraccion",
    "Percepcion",
    "Retencion",
    "Anticipo",
    "Company",
    "Branch",
    # Base
    "BaseDocument",
    "BaseSaleDocument",
    "NoteBase",
    # Documents
    "Invoice",
    "Boleta",
    "CreditNote",
    "DebitNote",
    "Quotation",
    "SaleNote",
    # Standalone
    "VoidedDocument",
    "DailySummary",
    "DispatchGuide",
    "DireccionGRE",
    "DetalleGRE",
    "Conductor",
    "Vehiculo",
    # Webhook
    "Webhook",
    # Responses
    "DocumentResponse",
    "VoidedResponse",
    "SummaryResponse",
]
