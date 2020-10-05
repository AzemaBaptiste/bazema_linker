import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd

from bazema_linker.utils.file_io import FileReader, FileWriter


class TestFileReader(unittest.TestCase):
    """
    Unit tests of file utils
    """

    def test_reader_constructor(self):
        file_reader = FileReader(path=Path('my/path/data.csv'))
        self.assertIsNotNone(file_reader)
        self.assertEqual(Path('my/path/data.csv'), file_reader.path)

    def test_read_drug_file_ok(self):
        file_reader = FileReader(path=Path('my/path/drugs.csv'))
        with patch('pandas.read_csv', MagicMock(return_value=pd.DataFrame(columns=['atccode', 'drug']))) \
                as mock_read_csv:
            file_reader.read_drug_file()
            mock_read_csv.assert_called()

    def test_read_drug_file_ko_filename_invalid(self):
        file_reader = FileReader(path=Path('my/path/not_drugs.csv'))
        file_reader.reject_file = MagicMock()
        with patch('pandas.read_csv', MagicMock()) as mock_read_csv, \
                self.assertLogs(file_reader.logger, level='ERROR') as cm:
            file_reader.read_drug_file()
            mock_read_csv.assert_not_called()
            file_reader.reject_file.assert_called_once()
            self.assertEqual(['ERROR:bazema_linker.utils.file_io:Can\'t process '
                              'file=my/path/not_drugs.csv - Invalid file name: '
                              'my/path/not_drugs.csv'], cm.output)

    def test_read_drug_file_ko_suffix_invalid(self):
        file_reader = FileReader(path=Path('my/path/drugs.qwerty'))
        file_reader.reject_file = MagicMock()
        with patch('pandas.read_csv', MagicMock()) as mock_read_csv, \
                self.assertLogs(file_reader.logger, level='ERROR') as cm:
            file_reader.read_drug_file()
            mock_read_csv.assert_not_called()
            file_reader.reject_file.assert_called_once()
            self.assertEqual(['ERROR:bazema_linker.utils.file_io:Can\'t process '
                              'file=my/path/drugs.qwerty - Invalid file name: '
                              'my/path/drugs.qwerty'], cm.output)

    def test_reject_file(self):
        file_reader = FileReader(path=Path('my/path/drugs.csv'))
        file_reader.move_a_file = MagicMock()

        file_reader.reject_file()

        file_reader.move_a_file.assert_called_once_with(target_folder=file_reader.REJECT_FOLDER)

    def test_move_file_archive(self):
        file_reader = FileReader(path=Path('my/path/drugs.csv'))
        file_reader.move_a_file = MagicMock()

        file_reader.move_file_archive()
        file_reader.move_a_file.assert_called_once_with(target_folder=file_reader.ARCHIVE_FOLDER)

    def test_move_a_file_mkdir(self):
        with patch("pathlib.Path.rename") as mock_path_rename, \
                patch("pathlib.Path.mkdir") as mock_path_mkdir, \
                patch("pathlib.Path.is_file", return_value=True):
            file_reader = FileReader(path=Path('my/path/drugs.csv'))
            file_reader.move_a_file('target')
            mock_path_mkdir.assert_called()
            mock_path_rename.assert_called_with(file_reader.path.cwd() /
                                                'target' / 'drugs.csv')


class TestFileWriter(unittest.TestCase):
    """
    Unit tests of Writer utils
    """

    def setUp(self):
        self.file_writer = FileWriter(path='my/path')

    def test_write_result(self):
        data = {'drug': 'the drug',
                'publications': ['pub1', 'pub2']
                }
        input_data = pd.DataFrame(data, columns=['drug', 'publications'])
        with patch("pandas.DataFrame.to_json") as mock_to_json, \
                patch("pathlib.Path.mkdir") as mock_path_mkdir:
            self.file_writer.write_result(input_data)
            mock_path_mkdir.assert_called()
            mock_to_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
