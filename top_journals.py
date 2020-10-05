import json
import sys
from collections import Counter


class TopJournals:
    def __init__(self):
        self.num_journals_aggregated = {}

    def update_counter_journal(self, agg_item):
        """Update aggregated dict with a new item"""
        if agg_item not in self.num_journals_aggregated:
            self.num_journals_aggregated.update({agg_item: 1})
        else:
            self.num_journals_aggregated[agg_item] = self.num_journals_aggregated[agg_item] + 1

    def compute_top_journal(self, result_filename: str):
        with open(result_filename) as result_file:
            result_json = json.load(result_file)

        for drug_item in result_json:
            journals_for_a_drug = [item['journal'] for item in drug_item['journal']]
            # converts to set - handle same drug with more than 1 publish to the same journal
            for journal in set(journals_for_a_drug):
                self.update_counter_journal(journal)

        # Get the top 1 journal
        top = Counter(self.num_journals_aggregated).most_common(1)[0]

        print(f'Journal with most different drugs is "{top[0]}" with a total of "{top[1]}" different drugs.')


if __name__ == '__main__':
    result_filename = sys.argv[1]
    TopJournals().compute_top_journal(result_filename)
