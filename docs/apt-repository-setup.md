# APT Repository Setup and Deployment Guide

This document provides a comprehensive guide for the APT repository implementation for rxiv-maker, including setup, maintenance, and troubleshooting.

## Overview

The rxiv-maker project now includes a fully automated APT repository system that provides Debian packages for Ubuntu and Debian users. The system includes:

- **Debian Packaging**: Complete `.deb` package generation
- **APT Repository**: Hosted via raw GitHub URLs with reprepro and GPG signing
- **Automated Publishing**: Integrated with release workflow
- **Multi-Architecture Support**: amd64, arm64, and architecture-independent packages

## Repository Structure

```
debian/                          # Debian packaging files
├── control                      # Package metadata and dependencies
├── changelog                    # Version history
├── rules                        # Build instructions (executable)
├── copyright                    # License information
├── compat                       # Debhelper compatibility level
├── source/
│   └── format                   # Source package format
├── rxiv-maker.install          # File installation mappings
├── rxiv-maker.postinst         # Post-installation script
└── rxiv-maker.prerm            # Pre-removal script

apt-repo/                        # APT repository configuration
├── conf/
│   ├── distributions           # Repository metadata
│   └── options                 # Repository options
└── README.md                   # Repository usage instructions

scripts/                         # Build and management scripts
├── build-deb.sh                # Debian package builder
└── setup-apt-repo.sh          # APT repository manager

.github/workflows/
├── publish-apt.yml             # APT publishing workflow
└── release-simple.yml          # Updated main release workflow
```

## Components

### 1. Debian Package Configuration

#### debian/control
- **Source package**: rxiv-maker
- **Section**: science (appropriate for scientific software)
- **Architecture**: all (Python package, platform-independent)
- **Dependencies**: Maps Python requirements to Debian packages
- **Recommends**: Optional but useful packages (Docker, R, Node.js)

#### debian/rules
- **Build system**: Uses debhelper with Python3 support
- **Build process**: Integrates with hatchling (Python build backend)
- **Testing**: Skips tests during package build (run in CI)
- **Documentation**: Installs examples and additional docs

#### Installation Scripts
- **postinst**: Updates TeX database, optional Playwright setup, verification
- **prerm**: Cleanup of temporary files (preserves user data)

### 2. APT Repository Infrastructure

#### Repository Metadata
- **Origin**: Rxiv-Maker Project
- **Distribution**: stable
- **Components**: main
- **Architectures**: amd64, arm64, all
- **Signing**: Mandatory GPG signing for security

#### Repository Structure
```
dists/stable/                    # Distribution metadata
├── main/
│   ├── binary-amd64/
│   ├── binary-arm64/
│   └── binary-all/
│       └── Packages             # Package index
├── Release                      # Repository metadata
└── Release.gpg                  # GPG signature

pool/main/                       # Package storage
└── r/rxiv-maker/
    └── rxiv-maker_*.deb        # Package files
```

#### reprepro Configuration

The APT repository uses reprepro for proper Debian repository management:

**Configuration Structure:**
```
apt-repo/
├── conf/
│   ├── distributions           # Repository distributions and settings
│   └── options                 # reprepro global options
├── incoming/                   # Temporary directory for new packages
├── dists/                      # Generated distribution metadata
├── pool/                       # Package pool storage
└── pubkey.gpg                  # Public GPG key for verification
```

**Key Features:**
- **Multi-Architecture Support**: Supports amd64, arm64, and architecture-independent packages
- **GPG Signing**: Automatic signing of repository metadata and packages
- **Raw GitHub Hosting**: Served directly via GitHub raw URLs for reliability
- **Automated Management**: Full integration with CI/CD workflows

### 3. GitHub Actions Integration

#### publish-apt.yml Workflow
**Jobs:**
1. **build-deb**: Builds Debian package from source
2. **setup-apt-repo**: Manages APT repository on apt-repo branch
3. **deploy-pages**: Publishes repository to GitHub Pages
4. **summary**: Provides comprehensive status reporting

**Security Features:**
- GPG key management via GitHub secrets
- OIDC authentication for GitHub Pages
- Signed packages and repository metadata

#### Integration with Release Workflow
- **Trigger**: After successful PyPI publication
- **Conditional**: Skipped in dry-run mode
- **Parallel**: Runs alongside Docker and Homebrew publishing
- **Status Reporting**: Integrated into release summary

## Installation Methods

### APT Repository (Recommended)
```bash
# Add GPG key
curl -fsSL https://raw.githubusercontent.com/henriqueslab/rxiv-maker/apt-repo/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/rxiv-maker.gpg

# Add repository
echo "deb [signed-by=/usr/share/keyrings/rxiv-maker.gpg] https://henriqueslab.github.io/rxiv-maker/ stable main" | sudo tee /etc/apt/sources.list.d/rxiv-maker.list

# Install
sudo apt update && sudo apt install rxiv-maker
```

### Direct Package Installation
```bash
# Download from GitHub releases
wget https://github.com/henriqueslab/rxiv-maker/releases/latest/download/rxiv-maker_1.5.10-1_all.deb

# Install with dpkg
sudo dpkg -i rxiv-maker_*.deb
sudo apt-get install -f  # Fix dependencies
```

## Build Scripts

### build-deb.sh
**Features:**
- Environment validation (checks for required tools)
- Version extraction from `__version__.py`
- Changelog generation with proper Debian format
- Package building with dpkg-buildpackage
- Lintian validation
- GPG signing support
- Comprehensive error handling and logging

**Usage:**
```bash
# Basic build
./scripts/build-deb.sh

# Clean build with signing
./scripts/build-deb.sh --clean --sign --key ABCD1234

# Custom output directory
./scripts/build-deb.sh --output /tmp/packages
```

### setup-apt-repo.sh
**Features:**
- Repository initialization
- Package addition to repository
- GPG key management
- Repository publishing to GitHub
- Metadata generation
- Git integration

**Usage:**
```bash
# Initialize repository
./scripts/setup-apt-repo.sh --init --key ABCD1234

# Add package
./scripts/setup-apt-repo.sh --deb dist/rxiv-maker_*.deb

# Update and publish
./scripts/setup-apt-repo.sh --update --publish
```

## Testing Framework

### Integration Tests (`tests/integration/test_apt_package.py`)
- Debian packaging file validation
- APT repository configuration testing
- Workflow syntax and structure validation
- Documentation completeness checks

### Unit Tests (`tests/unit/test_apt_scripts.py`)
- Build script functionality testing
- Repository script validation
- Workflow component testing
- Security and safety checks

### Test Categories
- **Platform-specific**: Tests that require specific tools
- **Integration**: End-to-end workflow testing
- **Unit**: Individual component testing
- **Security**: Safety and permission validation

## Security Considerations

### GPG Key Management
- **Private Key**: Stored in GitHub secrets (`APT_GPG_PRIVATE_KEY`)
- **Passphrase**: Stored in GitHub secrets (`APT_GPG_PASSPHRASE`)
- **Public Key**: Published in repository for verification

### Repository Security
- **Signed Packages**: All packages signed with GPG
- **Signed Repository**: Repository metadata signed
- **HTTPS**: Repository served over HTTPS via GitHub Pages
- **Key Verification**: Users must import GPG key for verification

### GitHub Actions Security
- **Minimal Permissions**: Only required permissions granted
- **Secret Management**: Sensitive data in GitHub secrets
- **OIDC**: Modern authentication for GitHub Pages
- **Workflow Isolation**: Separate workflow for APT operations

## Maintenance Procedures

### Regular Tasks
1. **Monitor builds**: Check workflow execution status
2. **Validate packages**: Ensure package integrity
3. **Update dependencies**: Keep Debian dependencies current
4. **Security updates**: Monitor for security advisories

### Troubleshooting

#### Build Failures
```bash
# Check build dependencies
sudo apt install debhelper dh-python dpkg-dev

# Validate packaging files
lintian --info debian/control

# Test build locally
./scripts/build-deb.sh --clean
```

#### Repository Issues
```bash
# Check repository structure
reprepro -b apt-repo list stable

# Validate GPG signatures
gpg --verify apt-repo/dists/stable/Release.gpg apt-repo/dists/stable/Release

# Re-export repository
reprepro -b apt-repo export
```

#### GitHub Actions Issues
- Check secret configuration in repository settings
- Verify workflow permissions
- Review job logs for specific error messages
- Test workflows with dry-run mode

### Version Updates
1. **Version is auto-detected** from henriqueslab/rxiv-maker repository during workflow execution
2. **Update changelog** in `debian/changelog`
3. **Test build locally** with `./scripts/build-deb.sh`
4. **Release through GitHub** triggers automated publication

## Performance Considerations

### Build Optimization
- **Parallel builds**: Use multiple CPU cores when available
- **Cached dependencies**: Reuse installed packages
- **Incremental builds**: Only rebuild when necessary

### Repository Optimization
- **Compression**: Use gzip and bzip2 compression
- **CDN**: GitHub Pages provides global CDN
- **Caching**: Proper HTTP caching headers

### Workflow Optimization
- **Conditional execution**: Skip unnecessary jobs
- **Artifact reuse**: Share build artifacts between jobs
- **Timeout management**: Prevent hanging builds

## Future Enhancements

### Planned Improvements
1. **Multi-distribution support**: Add support for different Ubuntu/Debian versions
2. **Automated testing**: Install packages in clean containers
3. **Mirror support**: Additional repository mirrors
4. **Package variants**: Different package configurations

### Integration Opportunities
1. **Launchpad PPA**: Official Ubuntu Personal Package Archive
2. **Debian packaging**: Official Debian package submission
3. **Snap packages**: Ubuntu Snap package support
4. **Flatpak**: Universal Linux package support

## Resources

### Documentation
- [Debian New Maintainers' Guide](https://www.debian.org/doc/manuals/maint-guide/)
- [Debian Policy Manual](https://www.debian.org/doc/debian-policy/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [reprepro Manual](https://mirrorer.alioth.debian.org/)

### Tools
- **debhelper**: Debian packaging helper tools
- **reprepro**: APT repository management
- **lintian**: Debian package checker
- **gpg**: GNU Privacy Guard for signing

### Community
- **Debian Mentors**: debian-mentors@lists.debian.org
- **Ubuntu Packaging**: ubuntu-packaging@lists.ubuntu.com
- **GitHub Actions Community**: github-community forum

---

This APT repository implementation provides a professional, secure, and maintainable distribution method for rxiv-maker on Debian and Ubuntu systems, following established best practices and security standards.