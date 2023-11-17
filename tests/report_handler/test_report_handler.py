import logging
import unittest
import sys
import pandas as pd
import os

from report_handler.report_handler import ReportHandler


class TestReportHandler(unittest.TestCase):

    # Setting up test environment and configure logging
    @classmethod
    def setUpClass(cls):
        print('Set Up - Configuring Logging')
        cls.format = '%(asctime)s  %(levelname)-9s  %(message)s'
        logging.basicConfig(
            level=logging.DEBUG, format=cls.format,
            filename="test_log.log")
        cls.console = logging.StreamHandler(sys.stderr)
        cls.formatter = logging.Formatter(cls.format)
        cls.console.setFormatter(cls.formatter)
        cls.console.setLevel(logging.DEBUG)
        logging.getLogger().addHandler(cls.console)

    def setUp(self) -> None:
        open("test_log.log", 'w')
        return super().setUp()

    def run_test_cases(self, verbose: bool = False):
        """
        This function runs the logging functions to test.
        """

        report_handler = ReportHandler(verbose)
        logging.getLogger().addHandler(report_handler)
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
        logging.info('{} - REJECT - some check.'.format(123), extra={})

        report_handler.write_report(file_path="./test_logs")

    def test_correct_sheets_generated(self):

        self.run_test_cases()

        # Reading the generated reporting and adding assertion checks
        for file in os.listdir("test_logs"):
            excel = pd.read_excel("test_logs/" + file, None)

            # Checks if two sheets generated
            sheets = len(excel.keys())
            self.assertEqual(2, sheets)

            # Removes files to avoid duplicate logging
            os.remove("test_logs/" + file)

    def test_correct_sheets_generated_with_verbose(self):

        self.run_test_cases(verbose=True)

        # Reading the generated reporting and adding assertion checks
        for file in os.listdir("test_logs"):
            excel = pd.read_excel("test_logs/" + file, None)

            # Checks if two sheets generated
            sheets = len(excel.keys())
            self.assertEqual(3, sheets)

            # Removes files to avoid duplicate logging
            os.remove("test_logs/" + file)

    def test_correct_data_in_sheet(self):
        self.run_test_cases()

        # Reading the generated reporting and adding assertion checks
        for file in os.listdir("test_logs"):
            excel = pd.read_excel("test_logs/" + file, None)

            # Gets the data from DEBUG sheet and check if logs as expected
            debug_data = excel["DEBUG"].values.flatten().tolist()
            col = excel["DEBUG"].columns.to_list()
            self.assertTrue(expr=["DEBUG" in col[0]])
            self.assertEqual(1, len(debug_data))
            unique_debug_data = set()
            for item in debug_data:
                unique_debug_data.add(item)
            self.assertEqual(
                ["123 - REJECT - no authors matched."],
                list(unique_debug_data))

            # Removes files to avoid duplicate logging
            os.remove("test_logs/" + file)

    def tearDown(self) -> None:
        os.remove("test_log.log")
        return super().tearDown()
