# File Cleanup and Cloud Storage Automation

## Overview

This comprehensive automation system helps you free up local disk space by intelligently identifying, compressing, and transferring files to secure cloud storage. The system prioritizes security with VPN verification, secure deletion, and comprehensive logging.

## Features

### 🔍 **Smart File Identification**
- Scans specified target folders
- Identifies large files and folders (>500MB)
- Calculates total space that can be freed
- Generates detailed size analysis

### 📦 **Intelligent Compression**
- Automatically compresses folders larger than 500MB
- Uses ZIP compression with configurable levels
- Maintains file integrity with hash verification
- Shows compression ratios and space savings

### ☁️ **Multi-Cloud Support**
- **Primary**: NordLocker (encrypted cloud storage)
- **Fallbacks**: Google Drive, Dropbox, pCloud, OneDrive
- Automatic detection of available cloud services
- Configurable priority order

### 🔒 **Security Features**
- VPN verification (NordVPN detection)
- Secure file deletion with multiple overwrite passes
- SHA256 hash verification for file integrity
- No credential storage in logs or scripts
- Encrypted cloud storage preference

### 📋 **Comprehensive Logging**
- Detailed execution logs (`file_cleanup.log`)
- Transfer summary (`files_transferred_log.txt`)
- File paths, sizes, hashes, and status tracking
- Error reporting and troubleshooting information

## Quick Start

### 1. Prerequisites
- Python 3.7 or higher
- NordVPN (recommended for security)
- At least one cloud storage service installed

### 2. Installation
```bash
# Clone or download the files
# Ensure all files are in the same directory:
# - file_cleanup_automation.py
# - run_file_cleanup.bat
# - cleanup_config.json
# - FILE_CLEANUP_README.md
```

### 3. Configuration
Edit `cleanup_config.json` to customize:
- Target folders to scan
- Compression threshold
- Cloud storage priority
- Security settings
- Backup options

### 4. Run the Automation
```bash
# Option 1: Use the batch file (Windows)
run_file_cleanup.bat

# Option 2: Run directly with Python
python file_cleanup_automation.py
```

## Configuration Options

### Target Folders
```json
"target_folders": [
    "~/Documents/YO-cosmetic",
    "~/Downloads/YO-assets",
    "~/Desktop/product-labels"
]
```

### Compression Settings
```json
"compression_threshold_mb": 500,
"advanced": {
    "compression_level": 6
}
```

### Cloud Storage Priority
```json
"cloud_storage_priority": [
    "nordlocker",
    "google_drive",
    "dropbox",
    "pcloud",
    "onedrive"
]
```

### Security Settings
```json
"security": {
    "require_vpn": true,
    "secure_deletion_passes": 3,
    "hash_algorithm": "sha256"
}
```

## How It Works

### 1. **Initialization**
- Checks VPN status (NordVPN)
- Loads configuration settings
- Validates target folders

### 2. **Scanning Phase**
- Scans each target folder recursively
- Calculates folder and file sizes
- Identifies items requiring compression (>500MB)
- Generates detailed inventory

### 3. **Processing Phase**
- Compresses large folders into ZIP files
- Calculates SHA256 hashes for integrity
- Uploads files to cloud storage (priority order)
- Verifies successful uploads

### 4. **Cleanup Phase**
- Securely deletes local copies (3-pass overwrite)
- Removes temporary compressed files
- Generates comprehensive logs

### 5. **Reporting**
- Creates detailed transfer log
- Shows space freed and items processed
- Reports any errors or issues

## Output Files

### `file_cleanup.log`
Detailed execution log including:
- VPN status verification
- Folder scanning results
- Compression progress
- Upload attempts and results
- Error messages and troubleshooting

### `files_transferred_log.txt`
Comprehensive transfer summary including:
- Total items processed
- Successfully uploaded items
- Space freed
- File hashes for verification
- Individual item status

## Security Considerations

### VPN Protection
- Automatically detects NordVPN
- Warns if VPN is not active
- Continues with user acknowledgment

### Secure Deletion
- 3-pass overwrite with random data
- File system sync for complete deletion
- Verification of deletion success

### Cloud Storage Security
- Prioritizes NordLocker (encrypted)
- No credential storage in scripts
- Uses local sync folders for uploads

## Troubleshooting

### Common Issues

**"Target folder does not exist"**
- Verify folder paths in configuration
- Use absolute paths if needed
- Check folder permissions

**"No cloud service detected"**
- Install at least one cloud storage service
- Ensure sync folders are accessible
- Check cloud service status

**"VPN not detected"**
- Start NordVPN before running script
- Verify NordVPN process is running
- Check VPN connection status

**"Upload failed"**
- Check cloud storage sync status
- Verify available disk space
- Check network connectivity

### Error Recovery
- Script continues processing other items on individual failures
- Detailed error logging for troubleshooting
- No data loss - files are only deleted after successful upload

## Advanced Usage

### Custom Cloud Storage
Add custom cloud storage paths to the configuration:
```json
"custom_cloud_paths": {
    "my_cloud": "~/MyCloudStorage"
}
```

### Backup Before Deletion
Enable backup creation:
```json
"backup": {
    "create_backup": true,
    "backup_location": "~/Backups/file_cleanup_backup"
}
```

### Performance Tuning
Adjust concurrent operations:
```json
"advanced": {
    "max_concurrent_uploads": 3,
    "upload_timeout_seconds": 300
}
```

## Best Practices

1. **Always use VPN** for secure transfers
2. **Test with small folders** before large operations
3. **Verify cloud uploads** before deletion
4. **Keep backup copies** of important files
5. **Monitor logs** for any issues
6. **Regular maintenance** of cloud storage

## Support

For issues or questions:
1. Check the log files for detailed error information
2. Verify all prerequisites are met
3. Test with a single small folder first
4. Ensure cloud storage services are properly configured

## License

This automation system is provided as-is for educational and personal use. Always test thoroughly before using on important data. 