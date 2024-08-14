# Test Environment for Disk Usage Monitoring Script

## Overview

This directory contains the test script designed to validate the functionality of the `disk_usage_monitor.sh` script in Task 1 of the Endurosat SRE Assessment. The test simulates high disk usage conditions on a mock filesystem and checks if the disk usage monitoring script correctly triggers an alert when the usage exceeds a specified threshold.

## Test Script: `test_disk_usage_monitoring.sh`

### Purpose

The `test_disk_usage_monitoring.sh` script is created to:

- Simulate a scenario where the disk usage on a temporary filesystem reaches a critical threshold.
- Execute the `disk_usage_monitor.sh` script to verify if it detects the high disk usage and sends an alert.
- Log the results of the test, indicating whether the monitoring script passed or failed.

### How It Works

1. **Setup**:

   - A temporary filesystem is created using a loopback device. This simulates a physical disk without affecting the actual disk on your machine.
   - The filesystem is mounted to a temporary directory (`/mnt/test`).

2. **Simulate Disk Usage**:

   - The script fills the temporary filesystem with data until the usage approaches the defined threshold, simulating a real-world scenario of high disk usage.

3. **Run the Monitoring Script**:

   - The main disk usage monitoring script (`disk_usage_monitor.sh`) is then executed to check if it correctly detects the high usage and triggers the appropriate alert.

4. **Validation**:

   - The script checks the log file (`/var/log/disk_usage_monitor.log`) to see if the monitoring script logged an alert. The presence of an alert log entry indicates that the test has passed.

5. **Cleanup**:
   - After the test is complete, the script unmounts the filesystem and removes the loopback device, ensuring that no temporary files or configurations remain on your system.

### Prerequisites

Before running the test script, ensure the following:

- You have sufficient permissions to create and manage loopback devices and mount filesystems. Running the script with `sudo` may be necessary.
- The `disk_usage_monitor.sh` script is located in the parent directory of the test environment (`../`).

### How to Run the Test

1. **Navigate to the test environment directory**:

   ```bash
   cd Endurosat-SRE-Assessment/Task1_Disk_Usage_Monitoring/test_environment/
   ```

2. **Ensure the test script is executable**:

   ```bash
   chmod +x test_disk_usage_monitoring.sh
   ```

3. **Run the test script**:

   ```bash
   ./test_disk_usage_monitoring.sh
   ```

### Expected Output

- Test Passed: If the disk_usage_monitor.sh script correctly identifies the high disk usage and logs the alert, the test will output:

  ```bash
  Test Passed: Disk usage alert was triggered correctly.
  ```

- Test Failed: If the script fails to trigger the alert, the test will output:
  ```bash
  Test Failed: Disk usage alert was not triggered.
  ```

### Log Files

- The disk_usage_monitor.sh script logs alerts to `/var/log/disk_usage_monitor.log`. The test script checks this log file to verify that an alert was triggered.

- Ensure that the log file is accessible and that your monitoring script is configured to write to this location.

### Troubleshooting

- Mount Point Issues: Ensure that the `/mnt/test` directory is not being used by other processes and that it exists before running the script.

- Permissions: If you encounter permission issues, try running the script with elevated privileges using sudo.

- Log File Location: Double-check that your monitoring script is writing logs to the correct file (`/var/log/disk_usage_monitor.log`). If the log file location is different, update the test script accordingly.

### Cleanup

The test script automatically handles cleanup by:

- Unmounting the temporary filesystem.
- Deleting the loopback device.
- Removing any temporary files created during the test.
- However, if the test script fails and does not complete the cleanup, you may need to manually unmount the filesystem and detach the loopback device:

  ```bash
  sudo umount /mnt/test
  sudo losetup -d /dev/loop0
  ```
