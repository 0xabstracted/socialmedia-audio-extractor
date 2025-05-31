# Scripts 🛠️

This directory contains utility scripts organized by functionality.

## 📁 Directory Structure

### 🚀 [deployment/](deployment/)
**Purpose:** Scripts for deploying the application to various environments

- **[deploy_to_aws.sh](deployment/deploy_to_aws.sh)** - Automated AWS EC2 deployment script
  - Sets up Docker environment
  - Configures firewall
  - Manages cookies
  - Builds and starts the application

**Usage:**
```bash
chmod +x scripts/deployment/deploy_to_aws.sh
./scripts/deployment/deploy_to_aws.sh
```

### 🍪 [cookies/](cookies/)
**Purpose:** Cookie management and authentication scripts

- **[refresh_cookies.py](cookies/refresh_cookies.py)** - Extract and validate YouTube cookies
  - Extracts cookies from Chrome/Firefox/Edge
  - Validates cookie functionality
  - Creates backup of existing cookies

**Usage:**
```bash
cd scripts/cookies
python3 refresh_cookies.py
```

### 🧪 [testing/](testing/)
**Purpose:** Testing and debugging utilities

- **[test_enhanced_api.py](testing/test_enhanced_api.py)** - API functionality testing
  - Tests info extraction
  - Tests audio extraction
  - Validates API responses

- **[debug_cookies.py](testing/debug_cookies.py)** - Cookie debugging utility
  - Checks cookie file existence
  - Validates cookie format
  - Tests cookie functionality

**Usage:**
```bash
# Test API functionality
cd scripts/testing
python3 test_enhanced_api.py

# Debug cookie issues
python3 debug_cookies.py
```

### 🔧 [utils/](utils/)
**Purpose:** Additional utility scripts (empty - for future expansion)

## 🎯 Common Usage Scenarios

### First Time Setup
1. **Deploy to AWS**: Run `deployment/deploy_to_aws.sh`
2. **Setup Cookies**: Run `cookies/refresh_cookies.py`
3. **Test API**: Run `testing/test_enhanced_api.py`

### Troubleshooting Bot Detection
1. **Debug Cookies**: Run `testing/debug_cookies.py`
2. **Refresh Cookies**: Run `cookies/refresh_cookies.py`
3. **Test Again**: Run `testing/test_enhanced_api.py`

### Regular Maintenance
```bash
# Weekly cookie refresh (recommended)
cd scripts/cookies && python3 refresh_cookies.py

# API health check
cd scripts/testing && python3 test_enhanced_api.py
```

## 📋 Requirements

### Python Dependencies
Most scripts require:
- Python 3.11+
- `requests` library
- `yt-dlp` (for cookie scripts)

### System Dependencies
- **Linux/macOS**: bash shell
- **Docker**: For deployment scripts
- **Browser**: Chrome, Firefox, or Edge (for cookie extraction)

## 🔒 Security Notes

- **Cookies contain sensitive data** - keep `cookies.txt` secure
- **Scripts may require elevated permissions** for system operations
- **Always review scripts** before running with elevated privileges

## 🚀 Making Scripts Executable

```bash
# Make deployment script executable
chmod +x scripts/deployment/deploy_to_aws.sh

# Make all scripts in a directory executable
chmod +x scripts/*/*.sh
```

## 📝 Adding New Scripts

When adding new scripts:
1. Choose the appropriate category folder
2. Add clear documentation comments in the script
3. Update this README with the new script
4. Follow the naming convention: `action_description.ext`

---

**Need help?** Check the main [README.md](../README.md) or specific documentation in [docs/](../docs/). 