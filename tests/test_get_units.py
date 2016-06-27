import unittest

from measurement.measures import Distance

from sphinx_measurement import process_measurement_string


class TestGetUnits(unittest.TestCase):
    def test_units_with_space(self):
        input_string = "100 m"

        expected_measurement = Distance(m=100)

        result = process_measurement_string(input_string)

        self.assertEqual(expected_measurement, result['measurement'])

    def test_units_without_space(self):
        input_string = "100m"

        expected_measurement = Distance(m=100)

        result = process_measurement_string(input_string)

        self.assertEqual(expected_measurement, result['measurement'])

    def test_referencing_a_stored_unit(self):
        input_string = "everest-height in inch"

        result = process_measurement_string(input_string)

        self.assertEqual('everest-height', result['reference'])
        self.assertEqual('inch', result['conversion_unit'])

    def test_stored_unit_identity(self):
        input_string = "100m as beep-boop"

        result = process_measurement_string(input_string)

        result = process_measurement_string(input_string)

        self.assertEqual(Distance(m=100), result['measurement'])
        self.assertEqual('beep-boop', result['identity'])
