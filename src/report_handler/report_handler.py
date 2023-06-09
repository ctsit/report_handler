import logging
import xlsxwriter
import os
from operator import itemgetter
from datetime import datetime
import report_handler.utils as utils


class ReportHandler(logging.Handler):

    # This handles the report logging instance and directs the output to the
    # report andn STDOUT
    def __init__(self, file_path):
        logging.Handler.__init__(self)
        self.logs = {}
        self.file_path = file_path

    def add_log_entries(self, record: logging.LogRecord, **kwargs):

        # set the default log message and sheet
        entry = self.log_msg
        sheet = record.levelname

        # add entry to sheet
        self.add_entry_to_sheet(sheet=sheet, entry=entry)

        # if additional information should be added
        if utils.containsKey(kwargs, "default_extras"):
            default_extras = kwargs.get("default_extras", {})
            extras = default_extras["default_extras"]

            sheet, entry = itemgetter("sheet", "content")(extras)

            # data, sheetname = utils.retrieve_data_and_sheet_name()

            self.add_entry_to_sheet(sheet=sheet, entry=entry)

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
                    headers, values = itemgetter("headers", "values")(row_data)
                    for col, value in enumerate(values):
                        worksheet.write(i + 1, col, value)
                elif not contains_header:
                    worksheet.write(i + 1, 0, row_data)
                    headers = [f"{sheet} log entries"]

            # write headers
            for i, header in enumerate(headers):
                worksheet.write(0, i, header)

        workbook.close()

    # Logging wouldn't work without overriding this method
    def emit(self, record):

        if not hasattr(self, "start_time"):
            self.start_time = datetime.utcnow()

        self.log_msg = record.msg
        self.log_msg = self.log_msg.strip()
        self.log_msg = self.log_msg.replace('\'', '\'\'')

        self.add_log_entries(record=record)
        
        if "report_handler" in record.__dict__.keys():
            entry, sheet = utils.retrieve_data_and_sheet_name(
                record.__dict__["report_handler"])

            headers, content = utils.get_headers_and_content(entry)
            default_extra = self.build_default_extras(
                headers=headers, content=content, sheet=sheet)

            self.add_log_entries(default_extras=default_extra, record=record)

    def get_today_date(self):
        return datetime.today().strftime('%Y-%m-%d')

    def build_default_extras(
            self, headers: list, content: list, sheet="") -> dict:
        return {
            'default_extras': {
                'sheet': sheet,
                'content': {
                    'headers': headers,
                    'values': content
                }
            }
        }
