# Backup and Restore Script

This Python script automates the process of backing up a local database, transferring it to a remote server, and restoring it on the remote database. The script also includes features like backup compression, checksum verification for file integrity, and automatic cleanup of old backups both locally and remotely. Logging with rotation is implemented to capture the script's activities and errors.

## Features

- Backup of MySQL or PostgreSQL databases
- Compresses backups into `.tar.gz` archives
- Transfers backups to a remote server via SCP
- Restores the database from the transferred backup on the remote server
- Checksum verification (`MD5` or `SHA256`) to ensure file integrity
- Automatic cleanup of old backups (both locally and remotely)
- Logs all actions and errors, with log rotation for managing file sizes
- Option to use password-based SSH authentication or SSH key-based authentication
- Ability to install missing dependencies like `sshpass` automatically

## Configuration

The script reads its configuration from a `config.json` file. The following fields are expected in the configuration:

```json
{
  "logging_level": "INFO", # The logging level, e.g., DEBUG, INFO, ERROR.
  "log_filename": "backup.log", # The name of the log file where logs will be written.
  "db_type": "mysql", # The type of the database (mysql or postgresql).
  "local_db_name": "your_local_db", # The local database name.
  "local_db_user": "your_local_db_user", # The local database user.
  "local_db_password": "your_local_db_password", # The local database password.
  "remote_host": "remote.server.com", # The remote server IP / Hostname.
  "remote_user": "remote_user", The remote server user for SSH connection.
  "remote_user_password": "remote_password", # The remote server user's password for SSH connection.
  "auth_method": "password",  # The method of authentication (password or ssh_key).
  "remote_host_ssh_key": "/path/to/ssh_key", # The path to the SSH key for authentication. If not provided, the script will attempt to use the default one.
  "remote_db_name": "your_remote_db", # The remote database name.
  "remote_db_user": "your_remote_db_user", # The remote database user.
  "remote_db_password": "your_remote_db_password", # The remote database password.
  "local_backup_dir": "/local/backup/directory", # Directory on the local server where backups are stored.
  "remote_backup_dir": "/remote/backup/directory", # Directory on the remote server where backups are stored.
  "backup_retention_count": 5, The number of backups to retain before older backups are deleted.
  "checksum_type": "md5",  # The type of checksum to use for file verification (md5 or sha256).
  "enable_checksum_verification": true, # Flag to enable/disable checksum verification.
  "subprocess_timeout": 300 # Timeout for subprocess commands (in seconds).
}
```

## Usage

- Clone the repository:
```bash
git clone https://github.com/vnedyalk0v/Endurosat-SRE-Assessment
cd Endurosat-SRE-Assessment/part-2_tasks/task2-db-backup
```

- Ensure your `config.json.example` file is renamed to `config.json` and properly set up with the required parameters.
- Run the script:
```bash
python3 backup_db.py
```

## Script Functions
- `check_and_install_sshpass()`: Ensures that sshpass is installed for password-based SSH authentication.
- `validate_ssh_key()`: Verifies the SSH key's validity by attempting a connection to the remote server.
- `validate_database_connection()`: Checks if the database connection is valid before proceeding with the backup.
- `backup_database()`: Creates a backup of the local database in `.sql` format.
- `compress_backup()`: Compresses the `.sql` file into a `.tar.gz` archive.
- `cleanup_old_backups()`: Deletes old local backups, retaining only the specified number of most recent backups.
- `cleanup_old_remote_backups()`: Removes old backups from the remote server, retaining only the specified number of backups.
- `create_remote_directory()`: Ensures that the remote backup directory exists.
- `transfer_backup()`: Transfers the compressed backup to the remote server using SCP.
- `verify_checksum()`: Verifies the integrity of the transferred backup using `MD5` or `SHA256` checksums.
- `restore_backup()`: Extracts the backup on the remote server and restores the database.

## Logging
The script logs its operations in a file specified by the `log_filename` configuration in `config.json` file, with log rotation enabled. The logs include information about backup success, transfer completion, and errors encountered during the process. Log messages are also output to the console.

## Error Handling
The script is designed to handle various errors, such as connection failures, missing dependencies, and checksum mismatches. These errors are logged, and appropriate error messages are raised for user attention.

## Dependencies

- `Linux OS` (`Debian`/`Ubuntu`, `CentOS`/`Rocky Linux`)
- `Python 3.x`
- `sshpass` (automatically installed if not present on the system)
- `mysqldump` or `pg_dump` for database backups
- `scp` for file transfers