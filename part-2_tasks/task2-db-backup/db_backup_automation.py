import os
import subprocess
import tarfile
import paramiko
import logging
import sys
from datetime import datetime

# Configuration
DB_NAME = "your_database_name"  # Name of the database to back up
DB_USER = "your_db_username"    # Database username
DB_PASSWORD = "your_db_password"  # Database password
DB_HOST = "localhost"  # Database host (usually localhost for local databases)
BACKUP_DIR = "/path/to/backup/directory"  # Directory to store backup files
ARCHIVE_NAME = "db_backup.tar.gz"  # Name of the compressed archive file
REMOTE_SERVER = "remote.server.com"  # Remote server address
REMOTE_USER = "remote_user"  # Username for SSH on the remote server
REMOTE_PATH = "/path/to/remote/backup/directory"  # Path on the remote server to store the backup
LOG_FILE = "/path/to/log/db_backup_automation.log"  # Path to the log file

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def backup_database():
    """Backup the specified database to a file."""
    try:
        # Construct the path for the backup file
        backup_file = os.path.join(BACKUP_DIR, f"{DB_NAME}.sql")
        
        # Command to dump the database to a SQL file
        dump_command = f"mysqldump -u {DB_USER} -p{DB_PASSWORD} -h {DB_HOST} {DB_NAME} > {backup_file}"
        
        # Execute the dump command
        subprocess.check_call(dump_command, shell=True)
        
        # Log the successful backup
        logging.info(f"Database backup successful: {backup_file}")
        return backup_file
    except subprocess.CalledProcessError as e:
        # Log the error if backup fails and exit
        logging.error(f"Database backup failed: {e}")
        sys.exit(1)

def compress_backup(backup_file):
    """Compress the database backup file into a .tar.gz archive."""
    try:
        # Construct the path for the compressed archive
        archive_path = os.path.join(BACKUP_DIR, ARCHIVE_NAME)
        
        # Open a tar.gz file and add the backup file to it
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(backup_file, arcname=os.path.basename(backup_file))
        
        # Log the successful compression
        logging.info(f"Backup file compressed successfully: {archive_path}")
        return archive_path
    except Exception as e:
        # Log the error if compression fails and exit
        logging.error(f"Failed to compress backup file: {e}")
        sys.exit(1)

def transfer_backup(archive_path):
    """Transfer the backup archive to a remote server using SSH."""
    try:
        # Initialize the SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the remote server
        ssh.connect(REMOTE_SERVER, username=REMOTE_USER)
        
        # Open an SFTP session
        sftp = ssh.open_sftp()
        
        # Define the remote file path
        remote_file_path = os.path.join(REMOTE_PATH, ARCHIVE_NAME)
        
        # Transfer the archive to the remote server
        sftp.put(archive_path, remote_file_path)
        
        # Close the SFTP session and SSH connection
        sftp.close()
        ssh.close()
        
        # Log the successful transfer
        logging.info(f"Backup archive transferred successfully to {REMOTE_SERVER}:{REMOTE_PATH}")
        return remote_file_path
    except Exception as e:
        # Log the error if transfer fails and exit
        logging.error(f"Failed to transfer backup archive: {e}")
        sys.exit(1)

def verify_transfer(local_file, remote_file):
    """Verify that the transferred file is not corrupted by comparing file sizes."""
    try:
        # Initialize the SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the remote server
        ssh.connect(REMOTE_SERVER, username=REMOTE_USER)
        
        # Open an SFTP session to get file size
        sftp = ssh.open_sftp()
        remote_size = sftp.stat(remote_file).st_size  # Get the size of the remote file
        local_size = os.path.getsize(local_file)  # Get the size of the local file
        
        # Close the SFTP session and SSH connection
        sftp.close()
        ssh.close()

        # Compare file sizes to ensure the transfer was successful
        if local_size == remote_size:
            logging.info("File verification successful: local and remote files match.")
            return True
        else:
            logging.error("File verification failed: local and remote files do not match.")
            sys.exit(1)
    except Exception as e:
        # Log the error if verification fails and exit
        logging.error(f"Failed to verify file transfer: {e}")
        sys.exit(1)

def restore_backup(remote_file):
    """Extract the archive on the remote server and restore the database."""
    try:
        # Initialize the SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
        # Connect to the remote server
        ssh.connect(REMOTE_SERVER, username=REMOTE_USER)
        
        # Commands to extract the archive and restore the database
        commands = [
            f"cd {REMOTE_PATH}",  # Change to the directory where the backup is located
            f"tar -xzf {remote_file}",  # Extract the archive
            f"mysql -u {DB_USER} -p{DB_PASSWORD} -h {DB_HOST} {DB_NAME} < {DB_NAME}.sql"  # Restore the database
        ]
        
        # Execute each command on the remote server
        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status != 0:
                logging.error(f"Command failed: {command}, Error: {stderr.read().decode()}")
                sys.exit(1)
        
        # Close the SSH connection
        ssh.close()
        
        # Log the successful restoration
        logging.info(f"Database restored successfully on remote server from {remote_file}")
    except Exception as e:
        # Log the error if restoration fails and exit
        logging.error(f"Failed to restore database: {e}")
        sys.exit(1)

def main():
    """Main function to perform the entire backup and restore process."""
    try:
        # Step 1: Backup the database
        backup_file = backup_database()

        # Step 2: Compress the backup
        archive_path = compress_backup(backup_file)

        # Step 3: Transfer the backup to the remote server
        remote_file = transfer_backup(archive_path)

        # Step 4: Verify the transfer
        if verify_transfer(archive_path, remote_file):
            # Step 5: Restore the database on the remote server
            restore_backup(remote_file)

    except Exception as e:
        # Log any unexpected errors and exit
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
