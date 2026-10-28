# WinPath Doctor

A light, zero-dependency Python tool to inspect, clean, deduplicate, and backup your PATH environment variables.

## Features

- **Analyze**: Detect duplicate entries and non-existent/invalid directory paths.
- **Normalize**: Remove unnecessary quotes, trailing slashes, and spaces.
- **Backup**: Create JSON snapshots of your PATH variable prior to making changes.
- **Export**: Generate clean PATH strings or direct PowerShell commands to update environment variables.

## Quick Start

Run directly with Python 3:

```bash
# Inspect current PATH environment variable
python -m winpath_doctor.cli

# Create a backup snapshot
python -m winpath_doctor.cli --backup

# List all backups
python -m winpath_doctor.cli --list-backups

# Output clean PATH string (valid paths only, deduplicated)
python -m winpath_doctor.cli --clean

# Generate PowerShell command to apply cleaned PATH
python -m winpath_doctor.cli --export-ps
```

## Running Tests

```bash
python -m unittest discover tests
```

---
_This project was scaffolded with the help of an AI agent._
