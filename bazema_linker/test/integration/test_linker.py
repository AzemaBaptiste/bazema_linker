import logging
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from bazema_linker.linker import Linker


class TestLinker(unittest.TestCase):

    def test_main(self):
        linker = Linker('data', 'output')
        linker.run_process = MagicMock()
        linker.main()

        linker.run_process.assert_called_once()

    def test_run_process(self):
        with patch("pathlib.Path.rename") as mock_path_rename, \
                patch("pathlib.Path.mkdir") as mock_path_mkdir, \
                patch('pandas.DataFrame.to_json') as mock_to_json:
            linker = Linker(Path(__file__).parent / 'test_data', 'result')
            result = linker.run_process()

            expected = [{'clinical_trials': [{'date': '1992-01-01', 'title': 'Use of drug1'},
                                             {'date': '2004-01-01', 'title': 'Use of drug1'},
                                             {'date': '2020-01-22', 'title': 'Use of drug1'}],
                         'drug': 'drug1',
                         'journal': [{'date': '1997-03-01', 'journal': 'journal 1'},
                                     {'date': '2004-04-01', 'journal': 'journal 1'},
                                     {'date': '2020-04-01', 'journal': 'journal 2'},
                                     {'date': '2020-01-01', 'journal': 'journal drugs 1 json'},
                                     {'date': '1992-01-01', 'journal': 'journal 1'},
                                     {'date': '2004-01-01', 'journal': 'journal 1'},
                                     {'date': '2020-01-22', 'journal': 'hôpital 2'}],
                         'pubmed': [{'date': '1997-03-01', 'title': 'Publish drug1'},
                                    {'date': '2004-04-01', 'title': 'Publish drug1'},
                                    {'date': '2020-04-01', 'title': 'Publish drug1'},
                                    {'date': '2020-01-01', 'title': 'Title drug1 json.'}]},
                        {'clinical_trials': [{'date': '2016-04-15', 'title': 'Drug2 as new'}],
                         'drug': 'drug2',
                         'journal': [{'date': '2002-12-30', 'journal': 'journal 2'},
                                     {'date': '2000-01-14', 'journal': 'journal drugs json'},
                                     {'date': '2016-04-15', 'journal': 'journal 2'}],
                         'pubmed': [{'date': '2002-12-30', 'title': 'Drug2 as new publication'},
                                    {'date': '2000-01-14', 'title': 'Title drug2 json'}]}]
            self.assertEqual(expected, result.to_dict(orient='records'))

            mock_to_json.assert_called_once()  # 1 write to output
            self.assertLogs(linker.logger, logging.INFO)  # only INFO logs


if __name__ == '__main__':
    unittest.main()
