"""Tests for DailySummary model."""

from datetime import date

from xfep.models.summary import DailySummary


class TestDailySummary:
    def test_valid_summary(self):
        s = DailySummary(
            company_id=1,
            branch_id=1,
            fecha_resumen=date(2026, 2, 17),
        )
        assert s.company_id == 1
        assert s.fecha_resumen == date(2026, 2, 17)
