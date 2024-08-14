# Endurosat Site Reliability Engineering (SRE) Assessment

## Overview

This repository contains solutions to the Site Reliability Engineering assessment provided by Endurosat. The assessment covers multiple tasks that demonstrate proficiency in system administration, automation, and CI/CD pipeline setup.

## Contents

### [Task 1: Disk Usage Monitoring](./Task1_Disk_Usage_Monitoring/README.md)

- **Objective**: Monitor disk usage on a Linux server and send alerts if usage exceeds a specified threshold.
- **Language**: Bash
- **Key Features**: Automated monitoring, email alerts, logging, cron job setup.
- **Files**:
  - `disk_usage_monitor.sh`: The main script.
  - `test_environment/`: Contains test scripts for validation.

### [Task 2: Database Backup Automation](./Task2_Database_Backup_Automation/README.md)

- **Objective**: Automate the process of backing up a database, compressing it, and transferring it to a remote server.
- **Language**: Python
- **Key Features**: Backup automation, SSH transfer, integrity checks, logging.
- **Files**:
  - `db_backup_automation.py`: The main script.
  - `test_environment/`: Contains test scripts for validation.

### [Task 3: Active Directory User Management](./Task3_AD_User_Management/README.md)

- **Objective**: Automate the creation, modification, and management of Active Directory user accounts.
- **Language**: PowerShell
- **Key Features**: User account automation, reporting, logging.
- **Files**:
  - `ad_user_management.ps1`: The main script.
  - `test_environment/`: Contains test scripts for validation.

### [Task 4: CI/CD Pipeline Setup](./Task4_CI_Pipeline_Setup/README.md)

- **Objective**: Set up a Continuous Integration (CI) pipeline for a simple web application.
- **Tools**: Docker, Jenkins (or another CI tool)
- **Key Features**: Automated builds, testing, and deployment.
- **Files**:
  - `simple_web_app/`: The web application with a `Dockerfile`.
  - `ci_pipeline_config.yml`: CI pipeline configuration file.
  - `Jenkinsfile`: Configuration file for Jenkins or equivalent.

## Getting Started

### Prerequisites

- Basic knowledge of Bash, Python, and PowerShell.
- Access to a Linux server for testing Task 1 and Task 2.
- A Windows environment for testing Task 3.
- CI tool (e.g., Jenkins, CircleCI) and Docker installed for Task 4.

### How to Use

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vnedyalk0v/Endurosat-SRE-Assessment.git
   ```
