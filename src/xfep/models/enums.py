"""SUNAT catalog enums for Peruvian electronic invoicing."""

from enum import StrEnum


class TipoDocumento(StrEnum):
    """Catálogo 01 — Tipo de documento."""

    FACTURA = "01"
    BOLETA = "03"
    NOTA_CREDITO = "07"
    NOTA_DEBITO = "08"
    GUIA_REMISION = "09"
    RETENCION = "20"
    PERCEPCION = "40"
    BAJA = "RA"
    RESUMEN = "RC"


class TipoDocIdentidad(StrEnum):
    """Catálogo 06 — Tipo de documento de identidad."""

    SIN_DOCUMENTO = "0"
    DNI = "1"
    CARNET_EXTRANJERIA = "4"
    RUC = "6"
    PASAPORTE = "7"


class TipoAfectacionIGV(StrEnum):
    """Catálogo 07 — Tipo de afectación al IGV."""

    GRAVADO = "10"
    GRAVADO_GRATUITO = "11"
    IVAP = "17"
    EXONERADO = "20"
    INAFECTO = "30"


class Moneda(StrEnum):
    """Catálogo 02 — Tipo de moneda."""

    PEN = "PEN"
    USD = "USD"


class TipoOperacion(StrEnum):
    """Catálogo 51 — Tipo de operación."""

    VENTA_INTERNA = "0101"
    ANTICIPOS = "0102"
    EXPORTACION_BIENES = "0200"
    EXPORTACION_SERVICIOS = "0201"
    NO_DOMICILIADOS = "0401"


class UnidadMedida(StrEnum):
    """Catálogo 03 — Unidad de medida (más usadas)."""

    UNIDAD = "NIU"
    SERVICIO = "ZZ"
    KILOGRAMO = "KGM"
    LITRO = "LTR"
    METRO = "MTR"
    CAJA = "BX"
    DOCENA = "DZN"
    GALON = "GLL"
    TONELADA = "TNE"


class MotivoNC(StrEnum):
    """Catálogo 09 — Motivo de nota de crédito."""

    ANULACION = "01"
    ANULACION_ERROR_RUC = "02"
    CORRECCION_DESCRIPCION = "03"
    DESCUENTO_GLOBAL = "04"
    DESCUENTO_ITEM = "05"
    DEVOLUCION_TOTAL = "06"
    DEVOLUCION_ITEM = "07"
    BONIFICACION = "08"
    DISMINUCION_VALOR = "09"
    OTROS = "10"
    AJUSTE_EXPORTACION = "11"
    AJUSTE_IVAP = "12"


class MotivoND(StrEnum):
    """Catálogo 10 — Motivo de nota de débito."""

    INTERESES_MORA = "01"
    AUMENTO_VALOR = "02"
    PENALIDADES = "03"
    OTROS = "10"
    AJUSTE_EXPORTACION = "11"
    AJUSTE_IVAP = "12"


class FormaPago(StrEnum):
    """Forma de pago."""

    CONTADO = "Contado"
    CREDITO = "Credito"


class MetodoEnvio(StrEnum):
    """Método de envío a SUNAT para boletas."""

    RESUMEN_DIARIO = "resumen_diario"
    DIRECTO = "directo"


class EstadoDocumento(StrEnum):
    """Estado interno del documento."""

    GENERADO = "GENERADO"
    ENVIADO = "ENVIADO"
    ACEPTADO = "ACEPTADO"
    RECHAZADO = "RECHAZADO"
    ANULADO = "ANULADO"


class EstadoSunat(StrEnum):
    """Estado del documento en SUNAT."""

    PENDIENTE = "PENDIENTE"
    ACEPTADO = "ACEPTADO"
    RECHAZADO = "RECHAZADO"
    ANULADO = "ANULADO"
