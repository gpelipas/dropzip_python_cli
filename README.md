# dropzip.py

Python script to zip files from a source folder and copy the resulting archive to a specified destination folder.

---

## Run with Environment Variables

```bash
export SOURCE_FOLDER=/path/to/source/folder
export DEST_FOLDER=/path/to/destination/folder
# overrides the default value of 'backup'
# zip will be named backup_YYYYMMDD_HHMMSS.zip
export ZIP_PREFIX=backup
# overrides the default value of false
export DELETE_AFTER_ZIP=true
# overrides the default value of empty (i.e. all files)
export ZIP_FILE_FILTER=
```

Then run without parameters:

```bash
python dropzip.py
```

---

## Run with Parameters

```bash
python dropzip.py --source /data/logs --dest /backups
python dropzip.py --source /data/logs --dest /backups --prefix ZYX
python dropzip.py --source /data/logs --dest /backups --prefix ZYX --delete true
python dropzip.py --source /data/logs --dest /backups --prefix ZYX --delete true --filter ".log"
```

---

## Parameters

| Parameter | Environment Variable | Default | Description |
|-----------|---------------------|---------|-------------|
| `--source` | `SOURCE_FOLDER` | *(required)* | Path to the source folder to zip |
| `--dest` | `DEST_FOLDER` | *(required)* | Path to the destination folder for the archive |
| `--prefix` | `ZIP_PREFIX` | `backup` | Prefix for the zip filename — output: `prefix_YYYYMMDD_HHMMSS.zip` |
| `--delete` | `DELETE_AFTER_ZIP` | `false` | Delete source files after zipping |
| `--filter` | `ZIP_FILE_FILTER` | *(empty — all files)* | File extension filter, e.g. `.log` |



