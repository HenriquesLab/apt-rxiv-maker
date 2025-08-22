# APT Repository User Guide

This comprehensive guide helps Ubuntu and Debian users install, update, and manage rxiv-maker through the official APT repository. The APT installation method provides the most seamless experience with automatic dependency management and easy updates.

## Quick Start

### One-Command Installation

```bash
# Add repository and install in one command block
curl -fsSL https://raw.githubusercontent.com/henriqueslab/rxiv-maker/apt-repo/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/rxiv-maker.gpg && \
echo "deb [signed-by=/usr/share/keyrings/rxiv-maker.gpg] https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo stable main" | sudo tee /etc/apt/sources.list.d/rxiv-maker.list && \
sudo apt update && sudo apt install rxiv-maker
```

### Verify Installation

```bash
# Check version
rxiv --version

# Validate installation
rxiv check-installation

# Create your first manuscript
rxiv init my-first-paper
cd my-first-paper
rxiv pdf
```

## Detailed Installation Guide

### Step 1: Add GPG Signing Key

The rxiv-maker APT repository is secured with GPG signatures. First, add the public key:

```bash
curl -fsSL https://raw.githubusercontent.com/henriqueslab/rxiv-maker/apt-repo/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/rxiv-maker.gpg
```

**What this does:**
- Downloads the GPG public key from the repository
- Converts it to binary format (`gpg --dearmor`)
- Stores it in the system keyring directory
- Uses `/usr/share/keyrings/` for modern APT key management

### Step 2: Add Repository Source

Add the rxiv-maker repository to your system's package sources:

```bash
# Recommended: Auto-detect architecture
echo "deb [signed-by=/usr/share/keyrings/rxiv-maker.gpg] https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo stable main" | sudo tee /etc/apt/sources.list.d/rxiv-maker.list

# Alternative: Architecture-specific installation
# For AMD64 (Intel/AMD 64-bit):
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/rxiv-maker.gpg] https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo stable main" | sudo tee /etc/apt/sources.list.d/rxiv-maker.list

# For ARM64 (Apple Silicon, ARM servers):
echo "deb [arch=arm64 signed-by=/usr/share/keyrings/rxiv-maker.gpg] https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo stable main" | sudo tee /etc/apt/sources.list.d/rxiv-maker.list

# Check your system architecture:
dpkg --print-architecture
```

**Repository details:**
- **URL**: `https://raw.githubusercontent.com/henriqueslab/rxiv-maker/apt-repo`
- **Distribution**: `stable`
- **Component**: `main`
- **Architectures**: `amd64`, `arm64`, `all`

### Step 3: Update Package Lists

Refresh your package database to include the new repository:

```bash
sudo apt update
```

**Expected output:**
```
Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease
Get:2 https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo stable InRelease [1,234 B]
Get:3 https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo stable/main amd64 Packages [567 B]
Get:4 https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo stable/main arm64 Packages [567 B]
Reading package lists... Done
```

### Step 4: Install rxiv-maker

Install the package and all its dependencies:

```bash
sudo apt install rxiv-maker
```

**Installation includes:**
- **Core Package**: rxiv-maker Python package with CLI tools
- **LaTeX Dependencies**: Essential LaTeX packages for document generation
- **Python Dependencies**: All required Python libraries
- **System Tools**: Supporting utilities and libraries
- **Documentation**: Example manuscripts and user guides

## Package Information

### What's Included

**Main Package (`rxiv-maker`):**
- Complete Python package with all modules
- Command-line interface (`rxiv` command)
- LaTeX style files and templates
- Example manuscripts
- Comprehensive documentation

**Essential Dependencies (Automatically Installed):**
```
# LaTeX packages
texlive-latex-base
texlive-latex-extra
texlive-fonts-recommended
biber

# Python dependencies
python3-matplotlib (>= 3.7.0)
python3-seaborn (>= 0.12.0)
python3-numpy (>= 1.24.0)
python3-pandas (>= 2.0.0)
python3-pil (>= 9.0.0)
python3-pypdf (>= 6.0.0)
python3-yaml (>= 6.0.0)
python3-click (>= 8.0.0)
python3-rich (>= 13.0.0)
python3-requests (>= 2.28.0)
python3-platformdirs (>= 4.0.0)
```

**Recommended Packages (Optional):**
```
# Container engines
docker.io | podman

# Development tools
nodejs (>= 16)
npm
r-base
git

# Enhanced LaTeX
texlive-full
pandoc
```

### Package Details

```bash
# View package information
apt show rxiv-maker

# List package files
dpkg -L rxiv-maker

# Check package dependencies
apt-cache depends rxiv-maker

# View package size and description
apt-cache show rxiv-maker
```

## Package Management

### Checking for Updates

```bash
# Check if updates are available
apt list --upgradable | grep rxiv-maker

# Show available versions
apt-cache policy rxiv-maker

# View package changelog
apt-get changelog rxiv-maker
```

### Updating rxiv-maker

```bash
# Update package lists
sudo apt update

# Upgrade rxiv-maker only
sudo apt install --only-upgrade rxiv-maker

# Upgrade all packages
sudo apt upgrade
```

### Version Management

```bash
# Install specific version
sudo apt install rxiv-maker=1.5.10-1

# Hold package at current version
sudo apt-mark hold rxiv-maker

# Unhold package for updates
sudo apt-mark unhold rxiv-maker

# Show held packages
apt-mark showhold
```

## Verification and Security

### GPG Signature Verification

```bash
# Verify repository GPG key
gpg --list-keys --keyring /usr/share/keyrings/rxiv-maker.gpg

# Check package signatures
apt-cache policy rxiv-maker

# Verify repository metadata
curl -s https://raw.githubusercontent.com/henriqueslab/rxiv-maker/apt-repo/dists/stable/Release.gpg | gpg --verify
```

### Package Integrity

```bash
# Verify package installation
dpkg -V rxiv-maker

# Check file permissions
find /usr -name "*rxiv*" -ls

# Validate Python package
python3 -c "import rxiv_maker; print('✅ Package import successful')"

# Test command functionality
rxiv --help
```

### Security Best Practices

1. **Always verify GPG signatures**: The repository is signed for security
2. **Use HTTPS**: Repository is served over encrypted connection
3. **Regular updates**: Keep package updated for security patches
4. **Monitor dependencies**: APT handles dependency security automatically

## Advanced Usage

### Multiple Versions

While APT typically manages one version, you can access different versions:

```bash
# List available versions
apt-cache madison rxiv-maker

# Install from different repository branch (if available)
sudo apt install -t testing rxiv-maker

# Downgrade to previous version
sudo apt install rxiv-maker=1.5.9-1
```

### Repository Management

```bash
# Disable repository temporarily
sudo mv /etc/apt/sources.list.d/rxiv-maker.list /etc/apt/sources.list.d/rxiv-maker.list.disabled
sudo apt update

# Re-enable repository
sudo mv /etc/apt/sources.list.d/rxiv-maker.list.disabled /etc/apt/sources.list.d/rxiv-maker.list
sudo apt update

# Remove repository completely
sudo rm /etc/apt/sources.list.d/rxiv-maker.list
sudo rm /usr/share/keyrings/rxiv-maker.gpg
sudo apt update
```

### Development Integration

```bash
# Install development dependencies
sudo apt install python3-dev build-essential

# Install optional enhanced features
sudo apt install texlive-full pandoc r-base nodejs npm

# Setup development environment
git clone https://github.com/henriqueslab/rxiv-maker.git
cd rxiv-maker
pip3 install -e .  # Development installation
```

## Troubleshooting

### Common Issues

**GPG Key Errors:**
```bash
# Error: "NO_PUBKEY" or signature verification failed
curl -fsSL https://raw.githubusercontent.com/henriqueslab/rxiv-maker/apt-repo/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/rxiv-maker.gpg
sudo apt update
```

**Repository Not Found:**
```bash
# Error: "404 Not Found" or repository unreachable
# Check internet connection
ping github.com

# Verify repository URL
curl -I https://raw.githubusercontent.com/henriqueslab/rxiv-maker/apt-repo/dists/stable/Release

# Check sources.list entry
cat /etc/apt/sources.list.d/rxiv-maker.list
```

**Dependency Conflicts:**
```bash
# Error: dependency resolution issues
sudo apt update
sudo apt install -f  # Fix broken packages
sudo apt autoremove  # Remove unnecessary packages

# For persistent issues
sudo apt install --fix-broken
```

**Package Not Found:**
```bash
# Error: "Unable to locate package rxiv-maker"
sudo apt update  # Refresh package lists
apt-cache search rxiv  # Search for package
cat /etc/apt/sources.list.d/rxiv-maker.list  # Verify sources
```

### Advanced Troubleshooting

**Debug APT Operations:**
```bash
# Verbose APT output
sudo apt install -o Debug::pkgAcquire::Worker=1 rxiv-maker

# Check APT logs
sudo tail -f /var/log/apt/history.log
sudo tail -f /var/log/apt/term.log

# Test repository connectivity
apt-cache policy
```

**Network and Proxy Issues:**
```bash
# Test direct repository access
wget -q --spider https://raw.githubusercontent.com/henriqueslab/rxiv-maker/apt-repo/dists/stable/Release

# Configure proxy for APT (if needed)
sudo nano /etc/apt/apt.conf.d/95proxies
# Add: Acquire::http::Proxy "http://proxy:port/";
```

**Package Validation:**
```bash
# Reinstall package cleanly
sudo apt remove rxiv-maker
sudo apt autoremove
sudo apt install rxiv-maker

# Verify package integrity
sudo dpkg --audit
sudo apt check
```

### Getting Help

**Diagnostic Information:**
```bash
# System information
lsb_release -a
uname -a

# APT configuration
apt-config dump

# Package status
dpkg -l | grep rxiv
apt-cache policy rxiv-maker

# Installation logs
grep rxiv /var/log/apt/history.log
```

**Support Channels:**
- **GitHub Issues**: https://github.com/henriqueslab/rxiv-maker/issues
- **Documentation**: https://github.com/henriqueslab/rxiv-maker#readme
- **Repository Status**: https://raw.githubusercontent.com/henriqueslab/rxiv-maker/apt-repo

## Uninstallation

### Complete Removal

```bash
# Remove package and dependencies
sudo apt remove rxiv-maker
sudo apt autoremove

# Remove configuration files
sudo apt purge rxiv-maker

# Remove repository
sudo rm /etc/apt/sources.list.d/rxiv-maker.list
sudo rm /usr/share/keyrings/rxiv-maker.gpg
sudo apt update
```

### Selective Removal

```bash
# Keep configuration, remove package
sudo apt remove rxiv-maker

# Remove package but keep dependencies
sudo apt remove --no-autoremove rxiv-maker

# Remove only automatically installed dependencies
sudo apt autoremove
```

## Migration from Other Installation Methods

### From PyPI Installation

```bash
# Remove PyPI installation
pip3 uninstall rxiv-maker

# Clean up any virtual environments
rm -rf ~/.local/lib/python*/site-packages/rxiv_maker*

# Install via APT
sudo apt install rxiv-maker
```

### From Source Installation

```bash
# Remove source installation
sudo rm -rf /usr/local/lib/python*/site-packages/rxiv_maker*
sudo rm -f /usr/local/bin/rxiv*

# Install via APT
sudo apt install rxiv-maker
```

### Configuration Migration

```bash
# User configurations are preserved in
~/.config/rxiv-maker/
~/.cache/rxiv-maker/

# No migration needed - configurations persist across installation methods
```

## Best Practices

### Regular Maintenance

1. **Weekly Updates**: Check for package updates regularly
2. **Security Monitoring**: Subscribe to security updates
3. **Dependency Cleanup**: Remove unused packages periodically
4. **Configuration Backup**: Backup important configurations

### Performance Optimization

1. **Cache Management**: APT cache is managed automatically
2. **Parallel Downloads**: APT handles parallel downloads
3. **Repository Distribution**: Raw GitHub URLs provide reliable global access
4. **Local Caching**: Consider `apt-cacher-ng` for multiple machines

### Integration with System

1. **System Integration**: Package integrates with system package manager
2. **Service Management**: No additional services required
3. **Path Management**: Commands automatically available in PATH
4. **User Permissions**: No special permissions required for normal use

## Comparison with Other Installation Methods

| Feature | APT Repository | PyPI (pip) | Source Build |
|---------|---------------|------------|-------------|
| **Dependency Management** | ✅ Automatic system deps | ❌ Manual system deps | ❌ All manual |
| **Security** | ✅ GPG signed packages | ⚠️ PyPI signing | ❌ No verification |
| **Updates** | ✅ Integrated with system | ⚠️ Manual updates | ❌ Manual tracking |
| **System Integration** | ✅ Full integration | ⚠️ Partial integration | ❌ Manual integration |
| **LaTeX Dependencies** | ✅ Automatic installation | ❌ Manual installation | ❌ Manual installation |
| **Installation Speed** | ✅ Fast (pre-built) | ⚠️ Medium (wheel) | ❌ Slow (compilation) |
| **Disk Usage** | ✅ Optimized | ⚠️ Average | ❌ Large (dev deps) |
| **Uninstallation** | ✅ Complete cleanup | ⚠️ Partial cleanup | ❌ Manual cleanup |

## Frequently Asked Questions

**Q: Is the APT package the same as the PyPI package?**
A: Yes, the APT package contains the same rxiv-maker software with additional system integration and dependency management.

**Q: Can I use both APT and pip installations?**
A: Not recommended. Choose one installation method to avoid conflicts.

**Q: How often is the APT repository updated?**
A: The repository is automatically updated with each rxiv-maker release.

**Q: Does the package work on Debian?**
A: Yes, the package is designed for both Ubuntu and Debian systems.

**Q: What if I need a newer version than available in APT?**
A: Check for updates with `apt update`. For cutting-edge features, consider the PyPI version.

**Q: Is internet connection required after installation?**
A: Only for downloading additional data (figures, citations) and updates. Core functionality works offline.

---

This guide provides everything you need to successfully install, manage, and use rxiv-maker through the APT repository system. For additional help, consult the main documentation or submit issues on GitHub.