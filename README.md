# Endurosat Site Reliability Engineering (SRE) Assessment

## Overview

This repository contains solutions to the Site Reliability Engineering assessment provided by Endurosat. The assessment covers multiple tasks that demonstrate proficiency in system administration, automation, and CI/CD pipeline setup.

## Contents

### [Open Questions](./part-1_open-questions/README.md)

- **Objective**: Provide detailed responses to questions on various topics, including Microsoft Active Directory, DHCP, Group Policy Objects, network troubleshooting, and more.
- **Format**: Markdown responses discussing relevant concepts, approaches, and best practices for each question.

### [Task 1: Disk Usage Monitoring](./part-2_tasks/task1-disk-usage/README.md)

- **Objective**: Monitor disk usage on a Linux server and send alerts if usage exceeds a specified threshold.
- **Language**: Bash
- **Key Features**: Automated disk usage monitoring, email alerts, logging, and cron job setup.
- **Files**:
  - `disk_usage_monitor.sh`: The main script.
  - `test_environment/`: Contains test scripts for validation.

### [Task 2: Database Backup Automation](./part-2_tasks/task2-db-backup/README.md)

- **Objective**: Automate the process of backing up a database, compressing it, and transferring it to a remote server.
- **Language**: Python
- **Key Features**: Automated backup creation, secure transfer via SSH, integrity checks, and logging.
- **Files**:
  - `db_backup_automation.py`: The main script.
  - `test_environment/`: Contains test scripts for validation.

### [Task 3: Active Directory User Management](./part-2_tasks/task3-ad-management/README.md)

- **Objective**: Automate the creation, modification, and management of Active Directory user accounts.
- **Language**: PowerShell
- **Key Features**: User account creation, modification, and reporting automation, with comprehensive logging.
- **Files**:
  - `ad_user_management.ps1`: The main script.
  - `test_environment/`: Contains test scripts for validation.

### [Task 4: CI/CD Pipeline Setup](./part-2_tasks/task4-ci-pipeline/README.md)

- **Objective**: Set up a Continuous Integration (CI) pipeline for a simple web application.
- **Tools**: Docker, Jenkins (or another CI tool)
- **Key Features**: Automated builds, testing, and deployment via a CI pipeline.
- **Files**:
  - `simple_web_app/`: The web application with a `Dockerfile`.
  - `ci_pipeline_config.yml`: CI pipeline configuration file.
  - `Jenkinsfile`: Jenkins pipeline configuration file.

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
