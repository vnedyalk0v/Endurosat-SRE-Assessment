#!/bin/bash
# This script tests the disk_usage_monitor.sh script by simulating high disk usage.

# Setup: Create a mock filesystem to test with
mkdir -p /tmp/test_disk_usage
dd if=/dev/zero of=/tmp/test_disk_usage/test.img bs=1M count=50
LOOP_DEVICE=$(losetup -f)
losetup $LOOP_DEVICE /tmp/test_disk_usage/test.img
mkfs.ext4 $LOOP_DEVICE

# Create the mount point directory if it doesn't exist
mkdir -p /mnt/test

# Mount the loop device to the mount point
mount $LOOP_DEVICE /mnt/test

# Fill the filesystem to simulate high disk usage
dd if=/dev/zero of=/mnt/test/fillfile bs=1M count=45

# Run the disk usage monitoring script and check if it triggers an alert
../disk_usage_monitor.sh

# Check the output (e.g., verify email was sent or log entry was made)
if grep -q "Alert sent" /var/log/disk_usage_monitor.log; then
    echo "Test Passed: Disk usage alert was triggered correctly."
else
    echo "Test Failed: Disk usage alert was not triggered."
fi

# Cleanup
umount /mnt/test
losetup -d $LOOP_DEVICE
rm -rf /tmp/test_disk_usage
