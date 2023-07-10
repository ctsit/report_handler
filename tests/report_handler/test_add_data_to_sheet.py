import unittest
import os
import pandas as pd
from report_handler.report_handler import ReportHandler


class TestAddDataToSheet(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # setting up the test data
        self.sheet = "test_sheet"
        self.data = {
            "headers": ["id", "failed_pub_check", "test_attribute"],
            "rows": [
                [1, "yes", "Test"],
                [2, "no", "tests"]
            ]
        }

        # Creating Handler object
        self.handler = ReportHandler()

    def test_add_data(self):

        # Write report
        self.handler.add_data_to_sheet(sheet=self.sheet, data=self.data, path="test_logs")

        for file in os.listdir("test_logs"):
            excel = pd.read_excel("test_logs/" + file, None)

            # Checks if one sheet is generated
            sheet = len(excel.keys())
            self.assertEqual(1, sheet)

            # Gets the data from sheet
            headers = excel[self.sheet].columns.to_list()
            rows = excel[self.sheet].values.tolist()

            # Gets data from test case
            headers_expected = self.data["headers"]
            rows_expected = self.data["rows"]

            # Check if both match
            self.assertEqual(headers, headers_expected)
            self.assertEqual(rows, rows_expected)

            # Removes files to avoid duplicate logging
            os.remove("test_logs/" + file)
