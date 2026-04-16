"""Tests for Webhook model."""

import pytest
from pydantic import ValidationError

from xfep.models.webhook import Webhook


class TestWebhook:
    def test_valid_webhook(self):
        w = Webhook(
            company_id=1,
            name="Webhook Principal",
            url="https://mi-servidor.com/webhook",
            events=["invoice.accepted", "invoice.rejected"],
        )
        assert w.name == "Webhook Principal"
        assert w.method == "POST"
        assert w.active is True

    def test_defaults(self):
        w = Webhook(
            company_id=1,
            name="Test",
            url="https://example.com/hook",
            events=["invoice.accepted"],
        )
        assert w.method == "POST"
        assert w.active is True

    def test_all_events_from_api_reference(self):
        w = Webhook(
            company_id=1,
            name="Webhook Principal",
            url="https://mi-servidor.com/webhook",
            method="POST",
            events=[
                "invoice.accepted", "invoice.rejected",
                "boleta.accepted", "boleta.rejected",
                "credit_note.accepted", "credit_note.rejected",
                "debit_note.accepted", "debit_note.rejected",
                "dispatch_guide.accepted", "dispatch_guide.rejected",
                "voided_document.sent", "voided_document.accepted", "voided_document.processed",
                "daily_summary.sent", "daily_summary.accepted", "daily_summary.processed",
            ],
            active=True,
        )
        assert len(w.events) == 16

    def test_custom_method(self):
        w = Webhook(
            company_id=1,
            name="PUT Hook",
            url="https://example.com/hook",
            method="PUT",
            events=["invoice.accepted"],
        )
        assert w.method == "PUT"

    def test_inactive_webhook(self):
        w = Webhook(
            company_id=1,
            name="Inactive",
            url="https://example.com/hook",
            events=["invoice.accepted"],
            active=False,
        )
        assert w.active is False

    def test_strips_whitespace(self):
        w = Webhook(
            company_id=1,
            name="  Webhook  ",
            url="https://example.com/hook",
            events=["invoice.accepted"],
        )
        assert w.name == "Webhook"
