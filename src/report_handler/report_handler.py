import logging
import xlsxwriter
import os
from datetime import datetime

import report_handler.utils as utils


class ReportHandler(logging.Handler):

    # This handles the report logging instance and directs the output to the
    # report andn STDOUT
    def __init__(self):
        logging.Handler.__init__(self)
        self.logs = {}

    def add_entry_to_sheet(self, sheet, entry):
        if sheet not in self.logs:
            self.logs[sheet] = [entry]
        else:
            self.logs[sheet].append(entry)

    def prevent_overwrite(self, filename):
        if not os.path.exists(filename):
            return filename

        name, extension = os.path.splitext(filename)

        count = 1

        new_filename = f'{name} ({count}){extension}'
        while os.path.exists(new_filename):
            count += 1
            new_filename = f'{name} ({count}){extension}'

        return new_filename

    def write_report(self, file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file = self.prevent_overwrite(
            f"{file_path}/report-{datetime.today().strftime('%Y-%m-%d')}.xlsx")

        workbook = xlsxwriter.Workbook(file)

        # Each log item is a new sheet
        for item in self.logs.items():
            headers = []
            sheet = item[0]
            rows_data = item[1]
            contains_header = isinstance(rows_data[0], dict)

            # create a new worksheet
            worksheet = workbook.add_worksheet(name=sheet)

            # write data
            for i, row_data in enumerate(rows_data):
                if contains_header:
                    headers, values = utils.get_headers_and_content(row_data)
                    for col, value in enumerate(values):
                        worksheet.write(i + 1, col, value)
                elif not contains_header:
                    worksheet.write(i + 1, 0, row_data)
                    headers = [f"{sheet} log entries"]

            # write headers
            for i, header in enumerate(headers):
                worksheet.write(0, i, header)

        workbook.close()

    def emit(self, record):
        # Only process if report_handler key is present
        if "report_handler" not in record.__dict__.keys():
            return

        if not hasattr(self, "start_time"):
            self.start_time = datetime.utcnow()

        # Add entry to levelname
        self.add_entry_to_sheet(sheet=record.levelname,
                                entry=self._clean_record_msg(record.msg))

        entry, sheet = utils.retrieve_data_and_sheet_name(
            record.__dict__["report_handler"])

        # Add to additional sheet if specified
        if (sheet):
            self.add_entry_to_sheet(sheet=sheet, entry=entry)

    def _clean_record_msg(self, raw_msg: str):
        cleaned_log_msg = raw_msg
        cleaned_log_msg = cleaned_log_msg.strip()
        return cleaned_log_msg
