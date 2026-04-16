"""Daily Summary (Resumen Diario) model."""

from datetime import date

from pydantic import BaseModel, ConfigDict


class DailySummary(BaseModel):
    """Resumen diario de boletas.

    Standalone model — does NOT extend BaseDocument.
    Batch operation model for sending boletas to SUNAT.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    company_id: int
    branch_id: int
    fecha_resumen: date
