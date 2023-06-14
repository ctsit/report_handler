import logging
import unittest
import sys
import pandas as pd
import os

from report_handler.report_handler import ReportHandler


class TestReportHandler(unittest.TestCase):

    # Setting up test environment and configure logging
    @classmethod
    def setUpClass(self):
        print('Set Up - Configuring Logging')
        self.format = '%(asctime)s  %(levelname)-9s  %(message)s'
        logging.basicConfig(
            level=logging.DEBUG, format=self.format,
            filename="test_log.log")
        self.console = logging.StreamHandler(sys.stderr)
        self.formatter = logging.Formatter(self.format)
        self.console.setFormatter(self.formatter)
        self.console.setLevel(logging.DEBUG)
        logging.getLogger().addHandler(self.console)
        self.report_handler = ReportHandler()
        logging.getLogger().addHandler(self.report_handler)

    def test_report_handler(self):

        # Example TestCasees

        # To check if logging in sheet as expected
        logging.debug('{} - REJECT - no authors matched.'.format(123),
                      extra={
            "report_handler": {
                'data': {'uid': 'xyz_reject', 'reason': 'no authors matched'},
                'sheet': 'author_checks',
            },
            "kafka": {
                'data': {'topic': 'logs'},
            },
            "sql": {
                'data': {'query': "SELECT * FROM TABLE"}
            }
        })

        # To check if entry not logged in sheet if "report_handler" signature not matched
        logging.debug('{} - REJECT - some check.'.format(123),
                      extra={
        })

        self.report_handler.write_report(file_path="test_logs")

        # Reading the generated reporting and adding assetion checks
        for file in os.listdir("test_logs"):
            excel = pd.read_excel("test_logs/"+file, None)

            # Checks if two sheets generated
            sheets = len(excel.keys())
            self.assertEqual(2, sheets)

            # Gets the data from DEBUG sheet and check if logs as expected
            debug_data = excel["DEBUG"].values.flatten().tolist()
            col = excel["DEBUG"].columns.to_list()
            self.assertTrue(expr=["DEBUG" in col[0]])
            self.assertEqual(2, len(debug_data))
            unique_debug_data = set()
            for item in debug_data:
                unique_debug_data.add(item)
            self.assertEqual(
                ["123 - REJECT - no authors matched."],
                list(unique_debug_data))

            # Removes files to avoid duplicate logging
            os.remove("test_logs/"+file)

        # Remove the Log file
        open("test_log.log", 'w').close()

        logging.info("INFO - Module log for some information")
        logging.debug("DEBUG - Module log for some debug")
        logging.warning("WARN - Module log for some warning")
        logging.error("ERROR - Module log for some error")

        log_sequence_expected = ["INFO", "DEBUG", "WARNING", "ERROR"]
        log_sequence = []

        # Open the generated logfile and check keywords for every log, matches them with
        # the expected sequence
        with open("test_log.log", "r") as log_file:
            for line in log_file:
                log_keyword = line[25:33]
                log_keyword = log_keyword.strip()
                log_sequence.append(log_keyword)
        self.assertEqual(log_sequence_expected, log_sequence)
        os.remove("test_log.log")


if __name__ == '__main__':
    unittest.main()
