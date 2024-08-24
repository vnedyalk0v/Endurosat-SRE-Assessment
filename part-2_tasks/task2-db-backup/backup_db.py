import os
import subprocess
import logging
import tarfile
import time
import glob
import json
from logging.handlers import RotatingFileHandler

# Load Configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# Configure Logging with log rotation and console output
log_level = getattr(logging, config['logging_level'].upper(), logging.INFO)
log_filename = config['log_filename']

# Create log file handler with rotation
log_handler = RotatingFileHandler(log_filename, maxBytes=5*1024*1024, backupCount=5)
log_handler.setLevel(log_level)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)

# Logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Adding handlers
logger = logging.getLogger()
logger.setLevel(log_level)
logger.addHandler(log_handler)
logger.addHandler(console_handler)

# Load other configurations from config.json
db_type = config['db_type']
local_db_name = config['local_db_name']
local_db_user = config['local_db_user']
local_db_password = config['local_db_password']

remote_host = config['remote_host']
remote_user = config['remote_user']
remote_user_password = config['remote_user_password']

auth_method = config['auth_method']
remote_host_ssh_key = config['remote_host_ssh_key']

remote_db_name = config['remote_db_name']
remote_db_user = config['remote_db_user']
remote_db_password = config['remote_db_password']

local_backup_dir = config['local_backup_dir']
remote_backup_dir = config['remote_backup_dir']

backup_retention_count = config['backup_retention_count']
checksum_type = config['checksum_type']
enable_checksum_verification = config.get('enable_checksum_verification', True)
subprocess_timeout = config.get('subprocess_timeout', 300)  # Timeout in seconds

# Validation for db_type and checksum_type
if db_type not in ['mysql', 'postgresql']:
    raise ValueError("Invalid database type. Supported types are 'mysql' and 'postgresql'")

if checksum_type not in ['md5', 'sha256']:
    raise ValueError("Invalid checksum type. Supported types are 'md5' and 'sha256'")

def check_and_install_sshpass():
    """
    Checks if sshpass is installed, and installs it if it's missing.
    """
    try:
        result = subprocess.run(['which', 'sshpass'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            logger.info("sshpass is already installed.")
            return
        else:
            logger.info("sshpass is not installed. Attempting to install...")

        distro = subprocess.run(['cat', '/etc/os-release'], stdout=subprocess.PIPE, text=True).stdout.lower()

        if 'ubuntu' in distro or 'debian' in distro:
            logger.info("Detected Ubuntu/Debian. Installing sshpass using apt-get...")
            subprocess.run(['apt-get', 'update'], check=True, timeout=subprocess_timeout)
            subprocess.run(['apt-get', '-y', 'install', 'sshpass'], check=True, timeout=subprocess_timeout)
        elif 'centos' in distro or 'rhel' in distro:
            logger.info("Detected CentOS/RHEL. Installing sshpass using yum...")
            subprocess.run(['yum', '-y', 'install', 'sshpass'], check=True, timeout=subprocess_timeout)
        elif 'fedora' in distro:
            logger.info("Detected Fedora. Installing sshpass using dnf...")
            subprocess.run(['dnf', '-y', 'install', 'sshpass'], check=True, timeout=subprocess_timeout)
        else:
            raise EnvironmentError("Unsupported distribution. Manual installation of sshpass is required.")
        logger.info("sshpass installation successful.")
    except subprocess.TimeoutExpired:
        logger.error(f"Timed out while trying to install sshpass.")
        raise
    except Exception as e:
        logger.error(f"Failed to install sshpass: {e}")
        raise

def validate_ssh_key():
    """
    Validates if the provided or default SSH key is correct by attempting a simple SSH connection.
    Logs an error if the key is incorrect.
    """
    try:
        ssh_key_option = f'-i {remote_host_ssh_key}' if remote_host_ssh_key else '-i ~/.ssh/id_rsa'
        test_ssh_command = f'ssh {ssh_key_option} {remote_user}@{remote_host} "echo Connection successful"'
        
        result = subprocess.run(test_ssh_command, shell=True, capture_output=True, text=True, timeout=subprocess_timeout)
        if "Connection successful" in result.stdout:
            logger.info("SSH key validation successful.")
        else:
            logger.error("SSH key validation failed. Invalid key or connection issue.")
            raise ValueError("SSH key validation failed.")
    except subprocess.CalledProcessError as e:
        logger.error(f"SSH key validation failed: {e}")
        raise
    except subprocess.TimeoutExpired:
        logger.error("SSH key validation timed out.")
        raise

def validate_database_connection():
    """
    Validates the connection to the database before backing up.
    """
    try:
        if db_type == 'mysql':
            validation_command = f'mysql -u {local_db_user} -p{local_db_password} -e "USE {local_db_name};"'
        elif db_type == 'postgresql':
            validation_command = f'psql -U {local_db_user} -d {local_db_name} -c "\q"'
        
        subprocess.run(validation_command, shell=True, check=True, timeout=subprocess_timeout)
        logger.info(f"Database validation successful: {local_db_name}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to validate database: {local_db_name}. Error: {e}")
        raise
    except subprocess.TimeoutExpired:
        logger.error("Database validation timed out.")
        raise

def backup_database():
    """
    Backs up the specified database to a SQL file in the local backup directory.
    """
    try:
        validate_database_connection()
        if db_type == 'mysql':
            backup_command = f'mysqldump -u {local_db_user} -p{local_db_password} {local_db_name} > {local_backup_dir}/{local_db_name}.sql'
        elif db_type == 'postgresql':
            backup_command = f'pg_dump -U {local_db_user} {local_db_name} > {local_backup_dir}/{local_db_name}.sql'
        else:
            raise ValueError("Invalid database type. Supported types are 'mysql' and 'postgresql'")
        
        subprocess.run(backup_command, shell=True, check=True, timeout=subprocess_timeout)
        logger.info(f"Database backup successful: {local_db_name}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Database backup failed: {e}")
        raise
    except subprocess.TimeoutExpired:
        logger.error("Backup process timed out.")
        raise

def compress_backup():
    """
    Compresses the SQL backup file into a .tar.gz archive in the local backup directory.
    A timestamp is appended to the archive name for uniqueness.
    """
    try:
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        archive_name = f'{local_db_name}_backup_{timestamp}.tar.gz'
        with tarfile.open(f'{local_backup_dir}/{archive_name}', 'w:gz') as tar:
            tar.add(f'{local_backup_dir}/{local_db_name}.sql', arcname=os.path.basename(f'{local_db_name}.sql'))
        os.remove(f'{local_backup_dir}/{local_db_name}.sql')
        logger.info(f"Backup compression successful: {archive_name}")
        return archive_name
    except Exception as e:
        logger.error(f"Backup compression failed: {e}")
        raise

def cleanup_old_backups(directory, backup_retention_count):
    """
    Removes old backups from the local directory, retaining only the specified number of backups.
    """
    try:
        backups = sorted(glob.glob(f"{directory}/*.tar.gz"), key=os.path.getmtime, reverse=True)
        for old_backup in backups[backup_retention_count:]:
            os.remove(old_backup)
            logger.info(f"Old backup removed: {old_backup}")
    except Exception as e:
        logger.error(f"Failed to clean up old backups: {e}")
        raise

def cleanup_old_remote_backups(remote_directory, backup_retention_count):
    """
    Removes old backups from the remote directory, retaining only the specified number of backups.
    Handles the case where there are no backups to delete.
    """
    try:
        if auth_method == 'ssh_key':
            ssh_key_option = f'-i {remote_host_ssh_key}' if remote_host_ssh_key else '-i ~/.ssh/id_rsa'
            list_command = f'ssh {ssh_key_option} {remote_user}@{remote_host} "ls -t {remote_directory}/*.tar.gz 2>/dev/null || echo no_backups"'
        elif auth_method == 'password':
            list_command = f'sshpass -p {remote_user_password} ssh {remote_user}@{remote_host} "ls -t {remote_directory}/*.tar.gz 2>/dev/null || echo no_backups"'

        result = subprocess.run(list_command, shell=True, capture_output=True, text=True, check=True)

        if "no_backups" in result.stdout or not result.stdout.strip():
            logger.info(f"No backups found in remote directory: {remote_directory}")
            return

        backups = result.stdout.splitlines()
        logger.info(f"Found {len(backups)} backups in remote directory: {remote_directory}")

        backups = sorted(backups, reverse=False)

        logger.info(f"Remote backups list (before cleanup): {backups}")

        for old_backup in backups[:-backup_retention_count]:
            if auth_method == 'ssh_key':
                delete_command = f'ssh {ssh_key_option} {remote_user}@{remote_host} "rm {old_backup}"'
            elif auth_method == 'password':
                delete_command = f'sshpass -p {remote_user_password} ssh {remote_user}@{remote_host} "rm {old_backup}"'

            subprocess.run(delete_command, shell=True, check=True)
            logger.info(f"Old remote backup removed: {old_backup}")

        logger.info("Remote backup cleanup completed successfully.")

    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to clean up old remote backups: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred during the cleanup of old remote backups: {e}")
        raise

def create_remote_directory():
    """
    Checks if the remote directory exists, and creates it if it does not.
    """
    try:
        if auth_method == 'ssh_key':
            # Use provided SSH key or default to ~/.ssh/id_rsa if not provided
            ssh_key_option = f'-i {remote_host_ssh_key}' if remote_host_ssh_key else '-i ~/.ssh/id_rsa'
            check_dir_command = f'ssh {ssh_key_option} {remote_user}@{remote_host} "mkdir -p {remote_backup_dir} && echo created || echo exists"'
        elif auth_method == 'password':
            check_dir_command = f'sshpass -p {remote_user_password} ssh {remote_user}@{remote_host} "mkdir -p {remote_backup_dir} && echo created || echo exists"'
        
        result = subprocess.run(check_dir_command, shell=True, capture_output=True, text=True, check=True, timeout=subprocess_timeout)
        if "created" in result.stdout:
            logger.info(f"Remote directory created: {remote_backup_dir}")
        else:
            logger.info(f"Remote directory already existed: {remote_backup_dir}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to create or check remote directory: {remote_backup_dir}, error: {e}")
        raise

def transfer_backup(archive_name):
    """
    Transfers the compressed backup archive to the remote server using SCP.
    """
    try:
        if auth_method == 'ssh_key':
            # Use provided SSH key or default to ~/.ssh/id_rsa if not provided
            ssh_key_option = f'-i {remote_host_ssh_key}' if remote_host_ssh_key else '-i ~/.ssh/id_rsa'
            transfer_command = f'scp {ssh_key_option} {local_backup_dir}/{archive_name} {remote_user}@{remote_host}:{remote_backup_dir}/{archive_name}'
        elif auth_method == 'password':
            transfer_command = f'sshpass -p {remote_user_password} scp {local_backup_dir}/{archive_name} {remote_user}@{remote_host}:{remote_backup_dir}/{archive_name}'
        
        subprocess.run(transfer_command, shell=True, check=True, timeout=subprocess_timeout)
        logger.info("Backup transfer successful")
    except subprocess.CalledProcessError as e:
        logger.error(f"Backup transfer failed: {e}")
        raise

def verify_checksum(local_file, remote_file):
    """
    Verifies the checksum of the local and remote backup files to ensure integrity.
    """
    try:
        if checksum_type == "md5":
            local_checksum = subprocess.run(f'md5sum {local_file}', shell=True, capture_output=True, text=True).stdout.split()[0]
            if auth_method == 'password':
                remote_checksum_command = f'sshpass -p {remote_user_password} ssh {remote_user}@{remote_host} "md5sum {remote_file}"'
            else:
                ssh_key_option = f'-i {remote_host_ssh_key}' if remote_host_ssh_key else '-i ~/.ssh/id_rsa'
                remote_checksum_command = f'ssh {ssh_key_option} {remote_user}@{remote_host} "md5sum {remote_file}"'
        elif checksum_type == "sha256":
            local_checksum = subprocess.run(f'sha256sum {local_file}', shell=True, capture_output=True, text=True).stdout.split()[0]
            if auth_method == 'password':
                remote_checksum_command = f'sshpass -p {remote_user_password} ssh {remote_user}@{remote_host} "sha256sum {remote_file}"'
            else:
                ssh_key_option = f'-i {remote_host_ssh_key}' if remote_host_ssh_key else '-i ~/.ssh/id_rsa'
                remote_checksum_command = f'ssh {ssh_key_option} {remote_user}@{remote_host} "sha256sum {remote_file}"'
        
        remote_checksum = subprocess.run(remote_checksum_command, shell=True, capture_output=True, text=True, timeout=subprocess_timeout).stdout.split()[0]
        
        if local_checksum == remote_checksum:
            logger.info("Checksum verification successful.")
        else:
            raise ValueError("Checksum mismatch! Possible data corruption.")
    except Exception as e:
        logger.error(f"Checksum verification failed: {e}")
        raise

def restore_backup(archive_name):
    """
    Extracts the backup archive on the remote server and restores the database.
    """
    try:
        if auth_method == 'ssh_key':
            ssh_key_option = f'-i {remote_host_ssh_key}' if remote_host_ssh_key else '-i ~/.ssh/id_rsa'
            extract_command = f'ssh {ssh_key_option} {remote_user}@{remote_host} "tar -xzf {remote_backup_dir}/{archive_name} -C {remote_backup_dir}"'
            if db_type == 'mysql':
                restore_command = f'ssh {ssh_key_option} {remote_user}@{remote_host} "mysql -u {remote_db_user} -p{remote_db_password} {remote_db_name} < {remote_backup_dir}/{local_db_name}.sql"'
        elif auth_method == 'password':
            extract_command = f'sshpass -p {remote_user_password} ssh {remote_user}@{remote_host} "tar -xzf {remote_backup_dir}/{archive_name} -C {remote_backup_dir}"'
            if db_type == 'mysql':
                restore_command = f'sshpass -p {remote_user_password} ssh {remote_user}@{remote_host} "mysql -u {remote_db_user} -p{remote_db_password} {remote_db_name} < {remote_backup_dir}/{local_db_name}.sql"'
        
        subprocess.run(extract_command, shell=True, check=True, timeout=subprocess_timeout)
        logger.info(f"Archive extraction successful: {archive_name}")
        
        subprocess.run(restore_command, shell=True, check=True, timeout=subprocess_timeout)
        logger.info("Database restore successful on remote server")
    except subprocess.CalledProcessError as e:
        logger.error(f"Database restore failed on remote server: {e}")
        raise
    except subprocess.TimeoutExpired:
        logger.error("Restore process timed out.")
        raise

if __name__ == "__main__":
    try:
        # Check if the log file already has content before logging the separator line
        if os.path.exists(log_filename) and os.path.getsize(log_filename) > 0:
            logger.info("---------------------------------------------------------------------")
        
        logger.info("===== Starting new backup and restore process =====")
        
        if auth_method == 'password':
            check_and_install_sshpass()

        if auth_method == 'auth_key':
            validate_ssh_key()

        backup_database()
        archive_name = compress_backup()
        create_remote_directory()
        transfer_backup(archive_name)
        if enable_checksum_verification:
            verify_checksum(f"{local_backup_dir}/{archive_name}", f"{remote_backup_dir}/{archive_name}")
        restore_backup(archive_name)
        cleanup_old_backups(local_backup_dir, backup_retention_count)
        cleanup_old_remote_backups(remote_backup_dir, backup_retention_count)

        logger.info("===== Backup and restore process completed =====")
    except KeyboardInterrupt:
        logger.error("Script manually interrupted by user (Ctrl + C).")
    except Exception as e:
        logger.error(f"An error occurred during the backup and restore process: {e}")
