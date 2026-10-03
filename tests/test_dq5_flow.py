import unittest
from pathlib import Path

from nds_rom_renamer.lib.identify import extract_serial
from nds_rom_renamer.lib.lookup import get_metadata
from nds_rom_renamer.lib.rename import build_filename


class DQ5FlowTests(unittest.TestCase):
    def test_dq5_rom_flow(self):
        rom_path = Path(__file__).with_name("DQ5.nds")

        serial = extract_serial(rom_path)
        self.assertEqual(serial, "YV5P")

        metadata = get_metadata(serial, str(rom_path.name))
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata["title"], "Dragon Quest: The Hand of the Heavenly Bride")
        self.assertEqual(metadata["region"], "EUR")
        self.assertEqual(metadata["languages"], ["EN", "FR", "DE", "ES", "IT"])

        filename = build_filename(
            metadata["title"],
            metadata["region"],
            metadata["languages"],
            serial,
            extension=".nds",
        )
        self.assertTrue(filename.startswith("Dragon Quest: The Hand of the Heavenly Bride"))
        self.assertIn("[EUR]", filename)
        self.assertIn("[YV5P]", filename)


if __name__ == "__main__":
    unittest.main()
