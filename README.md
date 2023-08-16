# report_handler

## About the project
This project helps separate the database and report logging from [`python_db_logger`](https://github.com/ctsit/python_db_logger) which requires a valid sql connection in order to log and generate a report. `report_handler` also adds the flexibility to the logger to add any number of handlers in order to send logs to different streams.

## Getting Started

There are two methods to install this package in your project,

- Using `pyproject.toml`:
  - Add `"report_handler @ git+https://git@github.com:/ctsit/report_handler.git"` in the `dependencies` section of the file.
  - Run `pip3 install .` to install in the virtual environment.
- Using `setup.py`:
  - Add `"report_handler @ git+https://git@github.com:/ctsit/report_handler.git"` in the `install_requires` section of the file.
  - Run `pip3 install .` to install in the virtual environment.

## Using the logger

### 1: Imports

Import the python `logging` module and `report_handler` using

```python
import logging
from report_handler.report_handler import ReportHandler
```

### 2: Creating logger instance

A root logger is created by the `logging` package and can be accessed anywhere accross the codebase using `logging.getLogger()`. Any changes to this affects logging accross the codebase.

Set the configuration for the logger as

```python
logging.basicConfig(
    level=logging.DEBUG,
    format=fmt,
    filename=file_name
)
```

The parameter definitions are:

- `level`: This is the logging level and denotes the severity of logs. Can take values as `logging.CRITICAL`, `logging.ERROR`, `logging.WARNING`, `logging.INFO`, `logging.DEBUG` or `logging.NOTSET`.

  - The severity levels are as follows:

    | Level    | Numeric value |
    | -------- | ------------- |
    | CRITICAL | 50            |
    | ERROR    | 40            |
    | WARNING  | 30            |
    | INFO     | 20            |
    | DEBUG    | 10            |
    | NOTSET   | 0             |

  - `format`: The format of the logs in the log file. An example format is
    `'%(asctime)s  %(levelname)-9s  %(message)s'`
  - `filename`: Log file path

### 3: Adding the handler and logging

This step includes getting the root logger and initializing the `report_handler` object and the adding it to the logger. This configures the root logger to pass the logs to `report_handler` also.

```python
report_handler = ReportHandler()
logger = logging.getLogger()
logger.addHandler(report_handler)
```

To log, call the following functions as required by the logging level:

```python
logging.debug(msg: str,extra: dict)
logging.warning(msg: str,extra: dict)
logging.info(msg: str,extra: dict)
logging.error(msg: str,extra: dict)
```

The parameter definitions are:

- `msg`: _Required._ The logging message.
- `extra`: _Optional_. This contains the handler and data information. The signature should match exactly as:

```python
{"report_handler": {
                    "data": {
                        'uid': uniqueid,
                        'reason': 'missing doi'
                        },
                    'sheet': 'pub_checks'
                    }
}
```

`"report_handler"` should have `"data"` and `"sheet"` as keys with the correspoding values.

Report handler also supports adding data using an array of entries using the `add_data_to_sheet` function:

```python
report_handler.add_data_to_sheet(
  sheet = "sheet_name",
  data = {
    "headers": ["id", "failed_pub_check"],
    "rows": [
      ["1", "yes"],
      ["2", "no"]
    ]
  }
)
```

The signature should match exactly as the example above

### 4: Generate report

At the very end of the program, generate the log `.xls` file using:

```python
report_handler.write_report(file_path="logs")
```
