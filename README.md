# Soccer Stats

A soccer statistics analysis tool that automatically updates and publishes data.

## Automated Daily Updates

The repository includes a GitHub Action that automatically updates and publishes soccer statistics data.

**Schedule:** The daily update action runs automatically every day at **12:00 UTC**.

**What it does:**
- Updates local soccer statistics data
- Uploads the updated data to the FTP server

**Manual Trigger:** The action can also be triggered manually through the GitHub Actions interface using the "workflow_dispatch" event.

**Configuration:** The action requires the following secrets to be configured in the repository:
- `FTP_SERVER`: FTP server address
- `FTP_USERNAME`: FTP username
- `FTP_PASSWORD`: FTP password
- `FTP_REMOTE_DIR`: Remote directory path on the FTP server