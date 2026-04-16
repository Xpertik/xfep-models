"""Tests for Company and Branch models."""

import pytest
from pydantic import ValidationError

from xfep.models.company import Branch, Company


class TestCompany:
    def test_valid_company_juridica(self):
        """RUC starting with '20' — persona jurídica."""
        c = Company(
            ruc="20123456789",
            razon_social="NUEVA EMPRESA S.A.C.",
            nombre_comercial="NUEVA EMPRESA",
            direccion="Av. Javier Prado 1234",
        )
        assert c.ruc == "20123456789"
        assert c.modo_produccion is False
        assert c.activo is True

    def test_valid_company_natural(self):
        """RUC starting with '10' — persona natural con negocio."""
        c = Company(
            ruc="10123456789",
            razon_social="PEREZ GARCIA JUAN",
        )
        assert c.ruc[:2] == "10"

    def test_invalid_ruc_prefix(self):
        """RUC with invalid prefix must be rejected."""
        with pytest.raises(ValidationError, match="10.*20"):
            Company(
                ruc="30123456789",
                razon_social="EMPRESA INVALIDA",
            )

    def test_ruc_too_short(self):
        with pytest.raises(ValidationError):
            Company(ruc="2012345", razon_social="EMPRESA")

    def test_ruc_too_long(self):
        with pytest.raises(ValidationError):
            Company(ruc="201234567890", razon_social="EMPRESA")


class TestBranch:
    def test_valid_branch(self):
        b = Branch(
            company_id=1,
            codigo="0001",
            nombre="Sucursal San Isidro",
            direccion="Av. Rivera Navarrete 501",
            ubigeo="150131",
        )
        assert b.codigo == "0001"
        assert b.company_id == 1

    def test_invalid_codigo_length(self):
        with pytest.raises(ValidationError):
            Branch(company_id=1, codigo="01", nombre="Sucursal")
