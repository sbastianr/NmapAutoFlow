# NetPulse Python

A modern desktop application for network scanning and reporting, built with Python and Flet.

## Features
- **Network Scanning**: Automates Nmap scans (Quick, Full, OS Detection).
- **Modern UI**: Dark mode interface built with Flet.
- **Reporting**: Generates PDF reports of scan results.
- **Portable**: Can be packaged into a single executable.

## Prerequisites
- **Python 3.8+**
- **Nmap**: Must be installed and added to your system PATH.
  - [Download Nmap](https://nmap.org/download.html)
  - Ensure `nmap` command works in your terminal.

## Installation

1. Clone the repository.
2. Create `requirements.txt` if not present (provided in repo).
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

1. Enter a target IP or range (e.g., `192.168.1.1`).
2. Select scan type.
3. Click **Start Scan**.
4. View results in the table or click **Export Report** to save as PDF.

## Building Executable

To create a standalone `.exe`:
```bash
pip install auto-py-to-exe
auto-py-to-exe
```
- Script Location: `main.py`
- Onefile: Yes
- Window Based: Yes
