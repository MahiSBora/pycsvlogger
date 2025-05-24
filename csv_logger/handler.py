import logging, csv
from pathlib import Path

class CsvLogHandler(logging.Handler):
    def __init__(self, filename, fieldnames=None):
        super().__init__()
        self.filename   = Path(filename)
        self.fieldnames = fieldnames or [
            "timestamp", "script", "record_id", "action", "status", "details"
        ]
        if not self.filename.exists():
            with self.filename.open("w", newline="") as f:
                csv.writer(f).writerow(self.fieldnames)

    def emit(self, record):
        # create a Formatter just to format our timestamp
        fmt    = logging.Formatter()
        datefmt = "%Y-%m-%d %H:%M:%S"

        row = []
        for col in self.fieldnames:
            if col == "timestamp":
                # uses Formatter.formatTime under the hood
                row.append(fmt.formatTime(record, datefmt))
            elif col == "status":
                row.append(record.levelname)
            elif col == "details":
                row.append(record.getMessage())
            elif col == "script":
                row.append(record.filename)   # source filename
            else:
                # any extra fields you bound, e.g. record_id, action, etc.
                row.append(getattr(record, col, ""))

        with self.filename.open("a", newline="") as f:
            csv.writer(f).writerow(row)
