from datetime import datetime
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from bazema_linker.utils.logging import get_logger


class FileReader:
    """
    Utils class managing read, parse and move of data files
    """
    REJECT_FOLDER = 'errors'
    ARCHIVE_FOLDER = 'archive'

    DRUG_FILE_NAME = 'drugs'
    PUBMED_FILE_NAME = 'pubmed'
    CLINICAL_TRIALS_FILE_NAME = 'clinical_trials'

    SUFFIX_CSV = '.csv'
    SUFFIX_JSON = '.json'

    def __init__(self, path: Path):
        self.path = Path(path)
        self.logger = get_logger(__name__)

    def read_drug_file(self) -> DataFrame:
        """TODO"""
        try:
            return self.read_file(valid_file_name=self.DRUG_FILE_NAME)
        except (ValueError, TypeError) as err:
            self.logger.error('Can\'t process file={} - {}'.format(self.path, err))
            return pd.DataFrame(columns=['atccode', 'drug'])  # returns empty dataframe

    def read_clinical_trials_file(self) -> DataFrame:
        """TODO"""
        try:
            return self.read_file(valid_file_name=self.CLINICAL_TRIALS_FILE_NAME)
        except (ValueError, TypeError) as err:
            self.logger.error('Can\'t process file={} - {}'.format(self.path, err))
            return pd.DataFrame(columns=['id', 'scientific_title',
                                         'date', 'journal'])  # returns empty dataframe

    def read_pubmed_file(self) -> DataFrame:
        """TODO"""
        try:
            return self.read_file(valid_file_name=self.PUBMED_FILE_NAME)
        except (ValueError, TypeError) as err:
            self.logger.error('Can\'t process file={} - {}'.format(self.path, err))
            return pd.DataFrame(columns=['id', 'title', 'date', 'journal'])  # returns empty dataframe

    def read_file(self, valid_file_name: str) -> DataFrame:
        """
        Parse valid files and returns content as a generator
        :return: Generator(tuple(country, user_id, sng_id))
        """
        if self.path.stem != valid_file_name:
            self.reject_file()
            raise ValueError(f'Invalid file name: {self.path}')

        self.logger.info('Reading file {}'.format(self.path))

        if self.path.suffix == self.SUFFIX_CSV:
            return pd.read_csv(self.path)
        elif self.path.suffix == self.SUFFIX_JSON:
            return pd.read_json(self.path, convert_dates=False, orient='records')
        else:
            self.reject_file()
            raise ValueError(f'Invalid file suffix: {self.path}')

    def reject_file(self):
        """Move invalid files to error folder"""
        self.move_a_file(target_folder=self.REJECT_FOLDER)

    def move_file_archive(self):
        """
        Move processed file to archive folder
        """
        self.move_a_file(target_folder=self.ARCHIVE_FOLDER)

    def move_a_file(self, target_folder: str):
        """Generic function to move files"""
        if not self.path.is_file():
            return

        if not (self.path.cwd() / target_folder).exists():
            (self.path.cwd() / target_folder).mkdir(parents=True)
        self.logger.info('Move file {} to {}.'.format(self.path, target_folder))
        self.path.rename(self.path.cwd() / target_folder / self.path.name)


# pylint: disable=too-few-public-methods
class FileWriter:
    """
    Utils class managing write of output files
    """

    def __init__(self, path):
        self._path = Path(path)
        self.logger = get_logger(__name__)

    def write_result(self, df_result: DataFrame):
        """
        Write result file
        :param df_result: dataframe to write
        """
        if not self._path.exists():
            self._path.mkdir(parents=True)

        date_now = datetime.now().date()
        output_filename = self._path / f'result_{date_now}.json'
        self.logger.info('Write results to {}'.format(output_filename))
        df_result.to_json(path_or_buf=output_filename, orient='records', indent=2)
