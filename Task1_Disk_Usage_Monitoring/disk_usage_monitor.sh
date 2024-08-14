#!/bin/bash

# Enable debugging mode (outputs each command before executing)
# set -x

### Start Configuration ###

# Disk usage threshold percentage that triggers an alert
THRESHOLD=80

# Recipient email address for disk usage alerts
EMAIL="root"

# Path to the log file where events will be recorded
LOGFILE="/var/log/disk_usage_monitor.log"

### End Configuration ###

# Find the path to the mail command (used for sending alerts)
MAIL_CMD=$(which mail)

# Function to send alert emails
send_alert() {
    local fs=$1           # Filesystem name
    local usage=$2        # Current disk usage percentage
    local mountpoint=$3   # Mount point of the filesystem
    local hostname=$(hostname)  # Get the hostname of the server

    # Prepare the subject and body of the email alert
    local subject="Disk Usage Alert on $hostname: $fs at ${usage}%"
    local body="Warning: The disk usage on $hostname for filesystem $fs mounted on $mountpoint has reached ${usage}%. Please take action.\n\nDetails:\nHostname: $hostname\nFilesystem: $fs\nMountpoint: $mountpoint\nUsage: ${usage}%"

    # Send the alert email and log the event
    echo -e "$body" | $MAIL_CMD -s "$subject" "$EMAIL"
    echo "Alert sent for $fs with usage at ${usage}%" >> "$LOGFILE"
}

# Function to check the disk usage of all filesystems
check_filesystems() {
    # Use df to get filesystem information, filtering for device-mounted filesystems
    df -h | grep '^/dev/' | while read -r line; do
        # Parse the filesystem, usage percentage, and mount point from the df output
        fs=$(echo $line | awk '{print $1}')
        usage=$(echo $line | awk '{print $5}' | sed 's/%//')
        mountpoint=$(echo $line | awk '{print $6}')

        # Log the current disk usage check with a timestamp
        echo "$(date) - Checking $fs mounted on $mountpoint: $usage% used" >> "$LOGFILE"

        # If the disk usage exceeds the threshold, send an alert and log the action
        if [ "$usage" -ge "$THRESHOLD" ]; then
            send_alert "$fs" "$usage" "$mountpoint"
            echo "$(date) - Alert sent for $fs at $usage% (Mountpoint: $mountpoint)" >> "$LOGFILE"
        fi
    done
}

# Execute the disk usage check function
check_filesystems

# Disable debugging mode
# set +x
