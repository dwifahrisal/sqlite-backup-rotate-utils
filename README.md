# sqlite-backup-rotate

Backup SQLite databases safely with `sqlite3 .backup` (safe even while the DB is in use) and automatically prune backups older than a configurable number of days.

## Usage

```bash
python3 backup.py app.db backups/
python3 backup.py app.db backups/ 14   # keep 14 days
```

## Cron example

```
30 2 * * * cd /path/to/repo && python3 backup.py app.db backups/
```
