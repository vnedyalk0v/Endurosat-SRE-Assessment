# Disk Usage Monitoring Script

This Bash script monitors the disk usage of the server's file systems and sends an email alert if the usage exceeds a specified threshold. It also logs all disk usage checks and any alerts sent to a log file. This script is designed to run as a cron job at a specified interval, ensuring continuous monitoring.

## Features

- **Threshold-based Alerts**: Sends an email alert if disk usage exceeds a predefined threshold.
- **Detailed Email Notifications**: Includes the server's hostname, affected filesystem, mount point, and usage percentage in the alert email.
- **Logging**: Records all disk usage checks and alerts to a log file for auditing and troubleshooting.
- **Configurable Parameters**: Easily customize the threshold, recipient email, and log file location.

## Requirements

- **Bash**: This script is written in Bash and should run on any Unix-like operating system.
- **mail**: The script uses the `mail` command to send email alerts. Ensure that the `mail` command is installed and configured to send emails on your system.
- **Cron**: To automate the script execution, it should be scheduled as a cron job.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://your-repository-url.git
   cd your-repository-directory
   ```

2. **Set Script Permissions**:
   Ensure the script is executable:

   ```bash
   chmod +x disk_usage_monitor.sh
   ```

3. **Configure the Script**:

   - **Threshold**: Adjust the `THRESHOLD` variable in the script to set the disk usage percentage that triggers an alert (default is 80%).
   - **Email**: Set the `EMAIL` variable to the system administrator's email address.
   - **Log File**: The `LOGFILE` variable defines where log entries will be stored (default is `/var/log/disk_usage_monitor.log`).

4. **Set Up Cron Job**:
   To run the script every 5 minutes, add the following line to your crontab:
   ```bash
   */5 * * * * /path/to/your/disk_usage_monitor.sh
   ```

## Usage

This script is intended to run automatically at regular intervals through cron. However, you can also execute it manually:

```bash
./disk_usage_monitor.sh
```
