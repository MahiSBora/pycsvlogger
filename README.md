# pycsvlogger

A **flexible, general-purpose CSV-based structured logging** library for Python’s built-in `logging` framework. It lets you emit rows of CSV with custom columns and automatically captured metadata—so you can track events (downloads, uploads, processing steps, etc.) across your entire codebase in one place.

---

## 🔧 Features

* **Configurable Columns**: Define exactly which CSV headers you want (e.g., `timestamp`, `script`, `record_id`, `action`, `status`, `details`, or any custom fields).
* **Automatic Metadata**: Captures log level (`status`), message (`details`), timestamp, and source script filename without extra code.
* **Context Binding**: Use a `LoggerAdapter` to bind default fields (e.g. `record_id`, `action`, `user`) once, then simply call `.info()`, `.error()`, etc., without repeating metadata.
* **No External Dependencies**: Built using only Python’s standard library (`logging`, `csv`, `pathlib`).
* **High Performance**: Appends rows to a single file—no per-record file sprawl.
* **Easy Analysis**: Load your CSV in Excel, Google Sheets, or use **Pandas** to filter, pivot, or visualize your logs.

---

## 🚀 Installation

Install from PyPI:

```bash
pip install pycsvlogger
```
---

## 🎯 Quickstart

1. **Initialize** the logger at your application’s entry point, choosing your CSV file and columns:

   ```python
   from csv_logger import init_csv_logger, get_record_logger

   init_csv_logger(
       log_file   = "Logs.csv",
       fieldnames = [
           "timestamp", "script", "record_id", "action", "status", "details"
       ]
   )
   ```

2. **Bind** a logger for each unit of work (e.g. per record or per processing step):

   ```python
   record_id = "abc123"
   logger    = get_record_logger(record_id=record_id, action="download")

   logger.info("Starting download from external API")
   # … perform download …
   logger.info("Download complete, saved to transcript.pdf")
   ```

3. **Switch Context** when you move to a new action or record:

   ```python
   # Same record, but now uploading link back
   logger = get_record_logger(record_id=record_id, action="upload_link")
   logger.info("Pushing download URL to record in service")
   # … perform PATCH …
   logger.info("Link updated successfully")
   ```

Your CSV (`logs/app_events.csv`) will look like:

```csv
timestamp,script,record_id,action,status,details
2025-05-24 11:00:05,main.py,abc123,download,INFO,Starting download from external API
2025-05-24 11:00:23,main.py,abc123,download,INFO,Download complete, saved to transcript.pdf
2025-05-24 11:01:10,main.py,abc123,upload_link,INFO,Pushing download URL to record in service
```

---

## ⚙️ Configuration Options

When you call `init_csv_logger`, you can customize:

* **`log_file`**: Path to your CSV log (default: `events.csv`).
* **`fieldnames`**: List of column headers in the order you want.

  * Supported automatic columns:

    * `timestamp` – formatted as `YYYY-MM-DD HH:MM:SS`
    * `status` – the log level (INFO, WARNING, ERROR, etc.)
    * `details` – your log message
    * `script` – the base filename of the calling module
  * **Custom columns**: any header names beyond the built‑in ones (`timestamp`, `status`, `details`, `script`) will be pulled from the keyword arguments you pass to `get_record_logger` (for example, `record_id="..."`, `action="..."`, `user="..."`). just pass all your headers like fieldnames = \[

    &#x20;       "timestamp", "script", "**record\_id**", "**action**", "status", "details"

    &#x20;   ], default + custom. 
* Once set, you don’t need to pass `record_id` or `action` on every log call—just bind them once with `get_record_logger`:

```python
# Bind multiple defaults at once:
logger = get_record_logger(record_id=rid, action="process", user="alice")
logger.info("Step 1: validation complete")
logger.info("Step 2: transformation started")
```

Those fields (`record_id`, `action`, `user`) will appear as columns in every row.

But whenever you have to assign a new record*id or action just pass them again. You can follow your own headers like username, employee*id e.t.c

---

## 🔍 Inspecting & Filtering Logs

Since your logs live in a single CSV file, you can easily:

* **Excel / Google Sheets**: Open and apply a filter on the `record_id` or `action` column.

* **Command line**:

  ```bash
  grep "abc123" logs/app_events.csv
  ```

* **Python / Pandas**:

  ```python
  import pandas as pd
  df = pd.read_csv("logs/app_events.csv")
  # Show only events for record abc123:
  print(df[df.record_id == "abc123"])

  # Count how many downloads succeeded:
  print((df[df.action == "download"].status == "INFO").sum())
  ```

This makes it trivial to drill down on failures, measure performance, or audit the full history for any ID.

---

## 💡 Advanced Tips

* **Error-level Logging**: When something goes wrong or you want to highlight warnings, use `logger.error("message")` or `logger.warning("message")`. These calls emit rows where the **status** column equals `ERROR` or `WARNING`, respectively, making it trivial to filter your CSV for all error events:

  ```python
  logger = get_record_logger(record_id=rid, action="download")
  try:
      download_file()
  except Exception as e:
      logger.error(f"Download failed: {e}")
  ```

* **Custom Metadata**: Bind any extra contextual information—such as `module`, `session_id`, `job_name`, or business-specific keys like `user_id` or `order_id`—by passing them as keyword arguments to `get_record_logger`. Ensure your `fieldnames` list includes these column names:

  ```python
  init_csv_logger(
      log_file="logs/events.csv",
      fieldnames=["timestamp","script","status","details","module","session_id"]
  )
  logger = get_record_logger(session_id="abc123", module="uploader")
  logger.info("Upload started")
  ```

* **Multiple Loggers**: If you need separate CSV files for different workflows, simply call `init_csv_logger` with different `log_file` paths early in each module.

*Happy logging!*
