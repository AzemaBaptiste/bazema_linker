import unittest

from bazema_linker.utils.parser import parse_args


class ParserTest(unittest.TestCase):

    def test_arguments(self):
        parsed = parse_args(['--input_dir', 'input',
                             '--output_dir', 'output'])

        self.assertEqual(parsed.input_dir, 'input')
        self.assertEqual(parsed.output_dir, 'output')

    def test_arguments_invalid(self):
        with self.assertRaises(SystemExit):
            parse_args(['--input_dir', 'input'])

    def test_arguments_invalid_no_args(self):
        with self.assertRaises(SystemExit):
            parse_args([])
