# APT Repository for Rxiv-Maker

[![APT Package Tests](https://github.com/HenriquesLab/apt-rxiv-maker/actions/workflows/test-apt-containers.yml/badge.svg)](https://github.com/HenriquesLab/apt-rxiv-maker/actions/workflows/test-apt-containers.yml)

This repository serves as a standalone APT repository for `rxiv-maker`, providing Debian/Ubuntu packages for easy installation and management.

## Quick Installation

### Ubuntu/Debian Systems

```bash
# Add GPG key
curl -fsSL https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/rxiv-maker.gpg

# Add APT repository (automatically detects architecture)
echo "deb [signed-by=/usr/share/keyrings/rxiv-maker.gpg] https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo stable main" | sudo tee /etc/apt/sources.list.d/rxiv-maker.list

# Update package list and install
sudo apt update
sudo apt install rxiv-maker
```

### Architecture-Specific Installation

For most users, the commands above will work automatically. If you need to specify architecture explicitly:

```bash
# For AMD64 (Intel/AMD 64-bit)
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/rxiv-maker.gpg] https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo stable main" | sudo tee /etc/apt/sources.list.d/rxiv-maker.list

# For ARM64 (Apple Silicon, ARM-based systems)
echo "deb [arch=arm64 signed-by=/usr/share/keyrings/rxiv-maker.gpg] https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo stable main" | sudo tee /etc/apt/sources.list.d/rxiv-maker.list

# Check your architecture
dpkg --print-architecture

# Universal script for any architecture
ARCH=$(dpkg --print-architecture)
echo "deb [arch=$ARCH signed-by=/usr/share/keyrings/rxiv-maker.gpg] https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo stable main" | sudo tee /etc/apt/sources.list.d/rxiv-maker.list
```

### Verify Installation

```bash
rxiv --version
rxiv --help
```

## Package Information

- **Package Name**: `rxiv-maker`
- **Architecture**: `all` (architecture-independent)
- **Distribution**: `stable`
- **Component**: `main`

### Dependencies

The package automatically handles installation of:
- Python 3.8+ runtime and libraries
- LaTeX distribution (texlive packages)
- Docker/Podman support (recommended)
- R and Node.js (recommended)

## Repository Structure

```
apt-rxiv-maker/
├── .github/workflows/     # GitHub Actions for testing and publishing
├── debian/               # Debian packaging control files
├── scripts/              # Build and management scripts
├── tests/                # APT testing infrastructure
├── apt-repo/             # Repository configuration
├── containerfiles/       # Container definitions for building
├── docs/                 # APT-specific documentation
└── README.md            # This file
```

## Development and Building

### Building Packages Locally

```bash
# Install build dependencies
sudo apt install debhelper dh-python python3-all python3-setuptools

# Build package
./scripts/build-deb.sh --clean --verbose

# Test package installation
sudo dpkg -i dist/rxiv-maker_*.deb
```

### Running Tests

```bash
# Run APT container tests
./scripts/test-apt-container.sh --ubuntu-version 22.04 --test-type installation

# Run validation tests
./scripts/validate-apt-repo.sh --repo-url "https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo"
```

### Repository Management

```bash
# Set up local APT repository
./scripts/setup-apt-repo.sh --init --key YOUR_GPG_KEY_ID

# Add package to repository
./scripts/setup-apt-repo.sh --deb dist/rxiv-maker_*.deb

# Update and publish repository
./scripts/setup-apt-repo.sh --update --publish
```

## CI/CD Pipeline

The repository uses GitHub Actions for:

- **Package Testing**: Automated testing across multiple Ubuntu versions
- **Repository Publishing**: Automated .deb building and APT repository updates
- **Security Validation**: Package security and integrity checks

### Workflows

1. **`test-apt-containers.yml`** - Comprehensive testing in containerized environments
2. **`publish-apt.yml`** - Automated package building and repository publishing

## Supported Platforms

- **Ubuntu**: 20.04 LTS, 22.04 LTS, 24.04 LTS
- **Debian**: 11 (Bullseye), 12 (Bookworm)
- **Architectures**: AMD64, ARM64

## Security

- All packages are GPG signed
- Repository metadata is cryptographically verified
- Regular security audits via automated testing

## Troubleshooting

### Common Issues

1. **GPG Key Import Fails**:
   ```bash
   # Alternative import method
   wget -qO - https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo/pubkey.gpg | sudo apt-key add -
   ```

2. **Repository Not Found**:
   - Verify internet connection
   - Check repository URL is accessible
   - Ensure GPG key is properly imported

3. **Dependency Issues**:
   ```bash
   # Fix broken dependencies
   sudo apt-get install -f
   
   # Update package cache
   sudo apt update
   ```

### Getting Help

- [Main Project Issues](https://github.com/henriqueslab/rxiv-maker/issues)
- [APT Repository Issues](https://github.com/HenriquesLab/apt-rxiv-maker/issues)
- [Documentation](./docs/)

## Contributing

1. Fork this repository
2. Create a feature branch
3. Make changes and test locally
4. Submit a pull request

### Testing Contributions

```bash
# Test your changes in a container
./scripts/run-container-tests.sh --ubuntu-versions "20.04,22.04,24.04" --test-types "installation,functionality"
```

## License

This repository follows the same license as the main rxiv-maker project. See the main repository for license details.

## Related Projects

- [rxiv-maker](https://github.com/henriqueslab/rxiv-maker) - Main project repository
- [homebrew-rxiv-maker](https://github.com/henriqueslab/homebrew-rxiv-maker) - Homebrew formula for macOS

---

For more information about rxiv-maker itself, visit the [main project repository](https://github.com/henriqueslab/rxiv-maker).