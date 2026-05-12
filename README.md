# AutoBrowserRefresher

A lightweight desktop tool that automatically refreshes one or more browser windows at a configurable interval. Targets windows by title substring so it works with any browser.

## Features

- Filter windows by comma-separated title substrings (e.g., `- Opera GX, - Chrome`)
- Configurable refresh interval in seconds
- Start/stop toggle in a simple Tkinter GUI
- Refresh loop runs in a background thread — UI stays responsive
- Cross-platform (Windows and macOS)

## Requirements

- Python 3.8+
- `pygetwindow`
- `pyautogui`

## Installation

```bash
# Install Python (Windows)
winget install -e --id Python.Python.3.12

# Install dependencies
pip install pygetwindow pyautogui
```

## Usage

```bash
python autocliker.py
```

1. Enter one or more window title substrings (comma-separated) matching the browser windows to refresh
2. Set the refresh interval in seconds
3. Click **Start** — all matching windows are refreshed on each tick
4. Click **Stop** to end the session
