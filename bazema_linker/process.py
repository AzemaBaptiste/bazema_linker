from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Any, Dict

import dateutil.parser
import pandas as pd
from pandas import DataFrame

from bazema_linker.utils.file_io import FileReader, FileWriter
from bazema_linker.utils.logging import get_logger

# pylint: disable=too-few-public-methods
class Process:
    """
    Computation class providing linking between drugs, pubmed, journal and clinical_trials
    """

    def __init__(self, data_folder, output_folder):
        self._data_folder = Path(data_folder)
        self._output_folder = Path(output_folder)
        self.logger = get_logger(__name__)

    def run_process(self) -> DataFrame:
        """
        Main process.
        Read data files. Aggregate relations between drugs, clinical trials,
        publications and journal.
        """

        # Parse drug file
        reader_drugs = FileReader(self._data_folder / 'drugs.csv')
        df_drugs = reader_drugs.read_drug_file()

        df_result = df_drugs.copy()
        df_result = df_result.drop(columns='atccode')

        # Process clinical trials
        reader_clinical_trials = FileReader(self._data_folder / 'clinical_trials.csv')
        df_clinical_trials = reader_clinical_trials.read_clinical_trials_file()
        df_clinical_trials.rename(columns={'scientific_title': 'title'}, inplace=True)
        df_result['clinical_trials'] = ProcessUtils().get_publication_infos(df_drugs, df_clinical_trials)

        # Process pubmed
        reader_pubmed_csv = FileReader(self._data_folder / 'pubmed.csv')
        reader_pubmed_json = FileReader(self._data_folder / 'pubmed.json')
        df_pubmed_csv = reader_pubmed_csv.read_pubmed_file()
        df_pubmed_json = reader_pubmed_json.read_pubmed_file()
        df_pubmed = pd.concat([df_pubmed_csv, df_pubmed_json])
        df_result['pubmed'] = ProcessUtils().get_publication_infos(df_drugs, df_pubmed)

        # Process journal
        df_result['journal'] = ProcessUtils().get_journal_infos(df_drugs, df_pubmed)

        # Write result
        FileWriter(self._output_folder).write_result(df_result)

        # Once everything is OK, move date files to archive
        reader_drugs.move_file_archive()
        reader_clinical_trials.move_file_archive()
        reader_pubmed_csv.move_file_archive()
        reader_pubmed_json.move_file_archive()

        return df_result


class ProcessUtils:
    """Utility class"""

    def __init__(self):
        self.logger = get_logger(__name__)

    def parse_date(self, date_str: str) -> str:
        """Parse string as date regardless of the formatting. Returns date ISO format."""
        try:
            return str(dateutil.parser.parse(date_str).date())
        except ValueError:
            self.logger.error('Can\'t parse date: %s', date_str)
            return ''

    @staticmethod
    def extract_items_matching(item: str, list_infos: List[Tuple[Any, ...]]) -> list:
        """TODO"""
        return list(filter(None, [infos if infos[0].lower().find(item.lower()) >= 0 else None for infos in list_infos]))

    def extract_publications_for_drug(self, drug: str,
                                      publications: List[Tuple[Any, ...]]) -> List[Dict[str, datetime]]:
        """TODO"""
        matching_publications = self.extract_items_matching(drug, publications)
        return [{'title': publication[0], 'date': self.parse_date(publication[1])}
                for publication in matching_publications]

    def extract_journals_for_drug(self, item, journals):
        """TODO"""
        matching_journals = self.extract_items_matching(item, journals)
        return [{'journal': journal[2], 'date': self.parse_date(journal[1])} for journal in matching_journals]

    def get_publication_infos(self, df_drugs: DataFrame, df_publications: DataFrame):
        """TODO"""
        tuple_trials = list(zip(df_publications.title, df_publications.date))
        return [self.extract_publications_for_drug(drug, tuple_trials) for drug in df_drugs.drug]

    def get_journal_infos(self, df_drugs: DataFrame, df_publications: DataFrame):
        """TODO"""
        tuple_trials = list(zip(df_publications.title, df_publications.date, df_publications.journal))
        return [self.extract_journals_for_drug(drug, tuple_trials) for drug in df_drugs.drug]
