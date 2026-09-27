# Elderly Care Support System

Desktop study project in Python and CustomTkinter for managing older-adult care information. It stores users, medication entries, routine activities, incidents and messages in a local SQLite database, with dashboard and report views. It is an organizational prototype, not a medical alert service.

## Run locally

Requires Python with a graphical desktop:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python ElderlyCareSystem.py
```

The SQLite file `cuidados_idoso.db` is created beside the script (or beside the packaged executable). Keep a backup of that file and use a writable directory. It contains personal information; do not commit a real database to a public repository.

## Scope and verification

The program has screens for entries, schedules, alerts, communication and reports. Reminders depend on the running application; the repository does not provide a background service or verified medical notifications. The Python source has been checked for syntax, but GUI behavior has not been tested here. Screenshots in this repository illustrate the project.

## Next evidence for a portfolio

Record a short walkthrough with sample, non-personal data and document a tested packaging command if distributing a Windows executable.
