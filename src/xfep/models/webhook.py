"""Webhook model."""

from pydantic import BaseModel, ConfigDict


class Webhook(BaseModel):
    """Webhook configuration for event notifications."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    company_id: int
    name: str
    url: str
    method: str = "POST"
    events: list[str]
    active: bool = True
