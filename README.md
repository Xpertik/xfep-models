# xfep-models

Modelos de datos Pydantic v2 para Facturación Electrónica en Perú (SUNAT UBL 2.1).

Paquete fundacional del [ecosistema XFEP](https://github.com/xpertik) — todos los demás paquetes dependen de este.

## Instalación

```bash
pip install xfep-models
```

## Modelos disponibles

### Documentos electrónicos (CPE SUNAT)

| Modelo | Módulo | Descripción |
|--------|--------|-------------|
| `Invoice` | `invoice` | Factura electrónica (serie F) |
| `Boleta` | `boleta` | Boleta de venta (serie B) |
| `CreditNote` | `credit_note` | Nota de crédito (serie FF/BB) |
| `DebitNote` | `debit_note` | Nota de débito (serie FD/BD) |
| `VoidedDocument` | `voided` | Comunicación de baja |
| `DailySummary` | `summary` | Resumen diario |
| `DispatchGuide` | `dispatch` | Guía de remisión electrónica (GRE) |

### Documentos internos (no SUNAT)

| Modelo | Módulo | Descripción |
|--------|--------|-------------|
| `Quotation` | `quotation` | Cotización (serie COT) |
| `SaleNote` | `sale_note` | Nota de venta (serie NV) |

### Entidades

| Modelo | Módulo | Descripción |
|--------|--------|-------------|
| `Client` | `client` | Cliente (persona o empresa) |
| `Company` | `company` | Empresa emisora (con credenciales SOL) |
| `Branch` | `company` | Sucursal / establecimiento anexo |
| `Detalle` | `detail` | Línea de detalle CPE (con IGV) |
| `DetalleSimple` | `detail` | Línea de detalle simplificado (NV/COT, sin IGV) |
| `VoidedDetail` | `detail` | Detalle de comunicación de baja |
| `GuiaVinculada` | `detail` | Guía de remisión vinculada |
| `Webhook` | `webhook` | Configuración de webhook |

### Modelos de pago

| Modelo | Módulo | Descripción |
|--------|--------|-------------|
| `CuotaPago` | `payment` | Cuota de pago al crédito |
| `Detraccion` | `payment` | Detracción SUNAT |
| `Percepcion` | `payment` | Percepción |
| `Retencion` | `payment` | Retención |
| `Anticipo` | `payment` | Anticipo |

### Modelos de respuesta

| Modelo | Módulo | Descripción |
|--------|--------|-------------|
| `DocumentResponse` | `responses` | Respuesta de creación de documento |
| `VoidedResponse` | `responses` | Respuesta de comunicación de baja |
| `SummaryResponse` | `responses` | Respuesta de resumen diario |

### Catálogos SUNAT (StrEnum)

| Enum | Valores clave |
|------|---------------|
| `TipoDocumento` | `FACTURA="01"`, `BOLETA="03"`, `NOTA_CREDITO="07"`, `NOTA_DEBITO="08"`, `GUIA_REMISION="09"` |
| `TipoDocIdentidad` | `SIN_DOCUMENTO="0"`, `DNI="1"`, `RUC="6"`, `PASAPORTE="7"` |
| `TipoAfectacionIGV` | `GRAVADO="10"`, `EXONERADO="20"`, `INAFECTO="30"`, `IVAP="17"` |
| `Moneda` | `PEN`, `USD` |
| `TipoOperacion` | `VENTA_INTERNA="0101"`, `EXPORTACION_BIENES="0200"` |
| `UnidadMedida` | `UNIDAD="NIU"`, `SERVICIO="ZZ"`, `KILOGRAMO="KGM"` |
| `FormaPago` | `CONTADO`, `CREDITO` |
| `MetodoEnvio` | `RESUMEN_DIARIO`, `DIRECTO` |
| `MotivoNC` | `ANULACION="01"`, `DEVOLUCION_ITEM="07"` |
| `MotivoND` | `INTERESES_MORA="01"`, `AUMENTO_VALOR="02"` |
| `EstadoDocumento` | `GENERADO`, `ENVIADO`, `ACEPTADO`, `RECHAZADO`, `ANULADO` |
| `EstadoSunat` | `PENDIENTE`, `ACEPTADO`, `RECHAZADO`, `ANULADO` |

## Uso

### Factura gravada

```python
from xfep.models import Invoice, Client, Detalle

invoice = Invoice(
    company_id=1,
    branch_id=1,
    serie="F001",
    fecha_emision="2026-02-10",
    moneda="PEN",
    tipo_operacion="0101",
    forma_pago_tipo="Contado",
    client=Client(
        tipo_documento="6",
        numero_documento="20123456789",
        razon_social="EMPRESA CLIENTE SAC",
    ),
    detalles=[
        Detalle(
            codigo="PROD001",
            descripcion="Laptop HP Pavilion 15.6",
            unidad="NIU",
            cantidad=1,
            mto_precio_unitario=2360,
            porcentaje_igv=18,
            tip_afe_igv="10",
        )
    ],
)
```

### Boleta de venta

```python
from xfep.models import Boleta, Client, Detalle

boleta = Boleta(
    company_id=1,
    branch_id=1,
    serie="B001",
    fecha_emision="2026-02-17",
    moneda="PEN",
    tipo_operacion="0101",
    metodo_envio="resumen_diario",
    client=Client(
        tipo_documento="1",
        numero_documento="67766554",
        razon_social="María Elena García",
    ),
    detalles=[
        Detalle(
            descripcion="Producto",
            unidad="NIU",
            cantidad=2,
            mto_precio_unitario=67,
            porcentaje_igv=18,
            tip_afe_igv="10",
        )
    ],
)
```

### Nota de crédito

```python
from xfep.models import CreditNote, Client, Detalle

nc = CreditNote(
    company_id=1,
    branch_id=1,
    serie="FF01",
    fecha_emision="2026-02-07",
    moneda="PEN",
    tipo_operacion="0101",
    tipo_doc_afectado="01",
    num_doc_afectado="F001-000047",
    cod_motivo="07",
    des_motivo="DEVOLUCION POR ITEM",
    client=Client(
        tipo_documento="6",
        numero_documento="20123456789",
        razon_social="EMPRESA SAC",
    ),
    detalles=[
        Detalle(
            descripcion="Producto devuelto",
            unidad="NIU",
            cantidad=1,
            mto_precio_unitario=100,
            porcentaje_igv=18,
            tip_afe_igv="10",
        )
    ],
)
```

### Comunicación de baja

```python
from xfep.models import VoidedDocument, VoidedDetail

baja = VoidedDocument(
    company_id=1,
    branch_id=1,
    fecha_referencia="2026-01-30",
    motivo_baja="ERROR EN CÁLCULO DE IGV",
    detalles=[
        VoidedDetail(
            tipo_documento="01",
            serie="F001",
            correlativo="000023",
            motivo_especifico="Error en IGV",
        )
    ],
)
```

## Validaciones incluidas

- **Serie prefix**: Invoice → `F`, Boleta → `B`, Quotation → `COT`, SaleNote → `NV`
- **NC/ND serie match**: `FF`/`BB` para NC, `FD`/`BD` para ND según doc afectado
- **Crédito requiere cuotas**: Si `forma_pago_tipo="Credito"`, debe incluir `forma_pago_cuotas`
- **Detalle mutual exclusion**: Usar `mto_precio_unitario` (con IGV) **o** `mto_valor_unitario` (sin IGV), nunca ambos
- **RUC prefix**: Company valida que RUC empiece con `10` o `20`
- **Detalles non-empty**: Todos los documentos requieren al menos 1 detalle

## Arquitectura

```
BaseDocument (campos compartidos)
├── Invoice      (serie F, client RUC)
├── Boleta       (serie B, metodo_envio)
├── NoteBase     (tipo_doc_afectado, cod_motivo)
│   ├── CreditNote  (serie FF/BB)
│   └── DebitNote    (serie FD/BD)
└── Quotation    (serie COT, dias_validez)

BaseSaleDocument (sin IGV, DetalleSimple)
└── SaleNote     (serie NV)

Standalone (sin herencia de BaseDocument)
├── VoidedDocument
├── DailySummary
└── DispatchGuide
```

## Desarrollo

```bash
# Clonar
git clone https://github.com/xpertik/xfep-models.git
cd xfep-models

# Instalar con dependencias de desarrollo
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Tests
pytest -v
```

## Stack

- **Python** >= 3.13
- **Pydantic** >= 2.0
- **Build**: Hatchling
- **Tests**: pytest + pytest-cov

## Parte del ecosistema XFEP

| Paquete | Descripción |
|---------|-------------|
| **xfep-models** | Modelos de datos (este paquete) |
| xfep-xml | Generación de XML UBL 2.1 |
| xfep-sign | Firma digital XML |
| xfep-ws | Cliente SOAP/REST para SUNAT |
| xfep-pdf | Generación de PDF |
| xfep-parser | Parseo de respuestas SUNAT (CDR) |
| xfep-consulta | Consulta integrada de CPE |
| xfep-lookup | Consulta RUC/DNI |
| xfep-gre | Guías de Remisión Electrónica |
| xfep-api | API REST (FastAPI) |
| xfep-dashboard | Panel de gestión (Django) |

## Licencia

MIT
