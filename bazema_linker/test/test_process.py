import unittest
from unittest.mock import patch

from bazema_linker.process import Process


class TestProcess(unittest.TestCase):
    def test_run_process(self):
        with patch("pathlib.Path.rename") as mock_path_rename, \
                patch("pathlib.Path.mkdir") as mock_path_mkdir, \
                patch('pandas.DataFrame.to_json'):
            Process('test_data', 'result').run_process()


if __name__ == '__main__':
    unittest.main()
