"""Tests for DispatchGuide model."""

from datetime import date

from xfep.models.dispatch import DispatchGuide


class TestDispatchGuide:
    def test_valid_dispatch(self):
        gre = DispatchGuide(
            company_id=1,
            branch_id=1,
            serie="T001",
            fecha_emision=date(2026, 2, 10),
            motivo_traslado="01",
            modalidad_transporte="01",
            peso_total=150.5,
            unidad_peso="KGM",
            punto_partida={
                "ubigeo": "150101",
                "direccion": "Av. Arequipa 123, Lima",
            },
            punto_llegada={
                "ubigeo": "040101",
                "direccion": "Calle Principal 456, Arequipa",
            },
            destinatario={
                "tipo_documento": "6",
                "numero_documento": "20123456789",
                "razon_social": "EMPRESA DESTINO SAC",
            },
            detalles=[
                {
                    "descripcion": "Carga general",
                    "unidad": "NIU",
                    "cantidad": 10,
                }
            ],
        )
        assert gre.serie == "T001"
        assert gre.peso_total == 150.5
        assert gre.punto_partida.ubigeo == "150101"
        assert gre.destinatario.razon_social == "EMPRESA DESTINO SAC"
