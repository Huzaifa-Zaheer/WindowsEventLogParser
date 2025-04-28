# Windows Event Log Parser

A simple and lightweight tool to parse, filter, and export Windows Event Logs (`.evtx` files) with both CLI and basic GUI support.

---

## Features

- Parse `.evtx` files and normalize the event data.
- Apply filters:
  - Event ID
  - Provider name
  - Start time / End time
- Export filtered events:
  - CSV format
  - JSON format
- Pretty printing of events using `tabulate`.
- Basic GUI to select file, apply filters, and export.

---

## Requirements

Install all required libraries using:

```bash
pip install -r requirements.txt
```

### Main Libraries Used:

- `pandas`
- `evtx`
- `tabulate`
- `tkinter` (comes built-in with Python)

---

## How to Run

### CLI Version

```bash
python main.py
```

### GUI Version

```bash
python gui.py
```

---

## Project Structure

```
WindowsEventLogParser/
├── data/
│   └── sample.evtx
├── filters/
│   └── filter.py
├── models/
│   └── event_model.py
├── parsers/
│   └── parser.py
├── main.py
├── gui.py
├── requirements.txt
├── README.md
```

---

##
