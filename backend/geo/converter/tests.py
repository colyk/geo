import json

from django.test import TestCase
import os.path as op
from .converter import Converter


class ConverterCase(TestCase):
    def setUp(self) -> None:
        fixtures_path = op.dirname(op.abspath(__file__))
        fixtures_path = op.join(fixtures_path, "fixtures")
        with open(op.join(fixtures_path, "test.json"), "r", encoding="utf-8") as f:
            self.test_geojson = f.read()
        with open(op.join(fixtures_path, "test.kml"), "r", encoding="utf-8") as f:
            self.test_kml = f.read()

        self.c = Converter()

    def test_geojson_to_kml(self):
        kml = self.c.geojson_to_kml(json.loads(self.test_geojson))
        self.assertEqual(kml, self.test_kml)

    def test_kml_to_geojson(self):
        geojson = self.c.kml_to_geojson(self.test_kml)
        self.assertEqual(geojson, json.loads(self.test_geojson))
