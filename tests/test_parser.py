import tempfile
import unittest
from pathlib import Path

from sciflex_cor_parser import CorFile


EXAMPLE_COR = """Speed (m/s)\tDeviation (µm)
1.7\t-13.7

Well No.=1M9
Nozzle No.=1
Camera Position=28630
Nozzle Z Offset=110
X Axis Position=34696
Y Axis Position=7579
Z Axis Position=28740
Nozzle Voltage [V]=45
Nozzle Pulse [µs]=sciPULSE_ULV02
Frequency [Hz]=500
Drop Volume [pl]=52
Volume StDev [%]=0.89
Unknown Setting=example

§01-06-32-03-52-50
"""


class CorFileTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary_directory.name)

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_reads_every_known_attribute(self):
        filename = self.directory / "example.cor"
        filename.write_text(EXAMPLE_COR, encoding="utf-8")

        cor_data = CorFile.from_file(str(filename))

        self.assertEqual(cor_data.speed, 1.7)
        self.assertEqual(cor_data.deviation, -13.7)
        self.assertEqual(cor_data.well_number, "1M9")
        self.assertEqual(cor_data.nozzle_number, 1)
        self.assertEqual(cor_data.camera_position, 28630)
        self.assertEqual(cor_data.nozzle_z_offset, 110)
        self.assertEqual(cor_data.x_axis_position, 34696)
        self.assertEqual(cor_data.y_axis_position, 7579)
        self.assertEqual(cor_data.z_axis_position, 28740)
        self.assertEqual(cor_data.nozzle_voltage, 45.0)
        self.assertEqual(cor_data.nozzle_pulse, "sciPULSE_ULV02")
        self.assertEqual(cor_data.frequency, 500.0)
        self.assertEqual(cor_data.drop_volume, 52.0)
        self.assertEqual(cor_data.volume_stdev, 0.89)
        self.assertEqual(cor_data.extra_attributes, {"Unknown Setting": "example"})

    def test_accepts_log_extension(self):
        filename = self.directory / "example.log"
        filename.write_text(EXAMPLE_COR, encoding="utf-8")

        self.assertEqual(CorFile.from_file(str(filename)).well_number, "1M9")

    def test_rejects_other_extensions(self):
        filename = self.directory / "example.txt"
        filename.write_text(EXAMPLE_COR, encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "File must be a .cor or .log file"):
            CorFile.from_file(str(filename))


if __name__ == "__main__":
    unittest.main()
