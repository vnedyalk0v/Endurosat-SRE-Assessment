# An Employee Has Left the Company, and Their Account Needs to Be Disabled Across All Systems. What Steps Would You Take to Ensure Their Access Is Revoked and Data Secured?

Ensuring that an employee’s access is revoked and their data is secured after they leave the company requires a systematic and thorough approach across all systems. Here’s how I would handle it:

### Step 1: Disable the User Account in Active Directory (AD)

- **Disable the AD Account**: In a Windows Active Directory environment, I would immediately disable the user’s account to prevent further access to the network and resources. This step cuts off access to domain-joined systems, shared folders, email, and other services.

  - **Example**: In Active Directory Users and Computers (ADUC), I would right-click the user’s account and select **Disable Account**. This ensures they cannot log in using their domain credentials.

### Step 2: Revoke Access to Email and Cloud Services

- **Revoke Email Access**: I would remove the employee’s access to their email account, whether hosted on-premises (e.g., Exchange) or in the cloud (e.g., Office 365, Gmail).

  - **Example**: For Office 365, I would disable the account via the Admin Center, ensuring the email address is no longer accessible.

- **Cloud and SaaS Applications**: I would also revoke access to any cloud services or SaaS applications (e.g., Google Workspace, Salesforce, Slack) the employee used, either by deactivating the account or removing their access through the administration panel.

### Step 3: Revoke Remote Access and VPN

- **Disable VPN Access**: I would revoke the employee’s VPN access by removing their account from the VPN system. This prevents the former employee from remotely connecting to the company network.

  - **Example**: In VPN management tools, I would delete or disable the user’s profile to ensure they no longer have remote access.

- **Remove Remote Access Accounts**: If the employee had remote access through other tools (e.g., RDP, SSH), I would remove their credentials and keys from the systems.

### Step 4: Secure Access to Company Devices

- **Retrieve Company Devices**: I would ensure that any company-issued devices (e.g., laptops, mobile phones) are returned. These devices should be locked or wiped remotely, if necessary, to ensure that sensitive data cannot be accessed.

  - **Example**: Using tools like Microsoft Intune or Apple’s Find My service, I would wipe the device remotely to protect company data.

- **Disable Local Accounts**: If the employee had local accounts on workstations or servers (e.g., admin accounts on Linux/Windows machines), I would disable or delete those accounts to prevent unauthorized access.

### Step 5: Review and Transfer Ownership of Data

- **Transfer Ownership**: I would transfer ownership of any important files, emails, or project data from the employee’s accounts to their manager or a designated team member to ensure business continuity.

  - **Example**: In Google Workspace, I would transfer document ownership to another user. In Office 365, I would grant access to the mailbox for review and ensure no critical emails are lost.

### Step 6: Remove Access from Third-Party Services

- **Audit Third-Party Accounts**: I would review and remove the employee’s access to any third-party services they used during their employment (e.g., project management tools, GitHub, cloud platforms).

  - **Example**: I would remove their SSH keys, API keys, or tokens from repositories like GitHub or cloud services like AWS/Azure to ensure they no longer have any control or access to these systems.

### Step 7: Update Security Groups and Permissions

- **Update AD Groups and Permissions**: I would remove the employee from all Active Directory groups and any shared folders or permissions that were assigned to them.

  - **Example**: I would review security group memberships and file system permissions to ensure that the former employee’s access is fully revoked.

### Step 8: Conduct an Audit of Access Logs

- **Audit Log Review**: To ensure that no suspicious activity occurred leading up to or after their departure, I would review access logs for any unauthorized or unusual access attempts.

  - **Example**: I would review logs from systems like the VPN, firewall, and email systems to verify that the employee did not access sensitive data after being notified of their departure.

### Step 9: Set Up a Final Check for Future Prevention

- **Create an Offboarding Checklist**: To ensure no step is missed in the future, I would establish a comprehensive offboarding checklist. This would include disabling accounts, recovering devices, transferring data, and revoking access to internal and third-party systems.

### Conclusion

Disabling an employee’s account and securing their data involves multiple steps across various systems. I would disable their Active Directory account, revoke access to email and cloud services, secure company devices, transfer ownership of important data, and review access logs for suspicious activity. Implementing a thorough offboarding process helps prevent unauthorized access and ensures data security across all platforms.
