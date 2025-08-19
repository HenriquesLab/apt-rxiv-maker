# APT Repository Installation

The rxiv-maker project provides an official APT repository for easy installation on Ubuntu and Debian systems.

## Quick Installation

```bash
# Add GPG key
curl -fsSL https://raw.githubusercontent.com/henriqueslab/rxiv-maker/apt-repo/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/rxiv-maker.gpg

# Add repository
echo "deb [signed-by=/usr/share/keyrings/rxiv-maker.gpg] https://henriqueslab.github.io/rxiv-maker/ stable main" | sudo tee /etc/apt/sources.list.d/rxiv-maker.list

# Update package list and install
sudo apt update && sudo apt install rxiv-maker
```

## Step-by-Step Installation

### 1. Add GPG Key

The repository is signed with a GPG key for security. Add the public key to your system:

```bash
curl -fsSL https://raw.githubusercontent.com/henriqueslab/rxiv-maker/apt-repo/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/rxiv-maker.gpg
```

### 2. Add Repository

Add the rxiv-maker APT repository to your system:

```bash
echo "deb [signed-by=/usr/share/keyrings/rxiv-maker.gpg] https://henriqueslab.github.io/rxiv-maker/ stable main" | sudo tee /etc/apt/sources.list.d/rxiv-maker.list
```

### 3. Update Package Lists

Update your package lists to include packages from the new repository:

```bash
sudo apt update
```

### 4. Install rxiv-maker

Install rxiv-maker and all its dependencies:

```bash
sudo apt install rxiv-maker
```

## Package Information

The APT package includes:

- **rxiv-maker**: Main Python package with CLI tools
- **LaTeX dependencies**: Essential LaTeX packages for document generation
- **System dependencies**: Required system libraries and tools
- **Documentation**: Example manuscripts and usage guides
- **Templates**: LaTeX style files and templates

### Dependencies Installed

**Essential LaTeX packages:**
- `texlive-latex-base`
- `texlive-latex-extra` 
- `texlive-fonts-recommended`
- `biber`

**Python dependencies:**
- All required Python packages from PyPI
- Matplotlib, pandas, numpy for figure generation
- Rich CLI libraries for enhanced output

**Recommended packages (optional):**
- `docker.io` or `podman` for containerized execution
- `nodejs` and `npm` for JavaScript-based tools
- `r-base` for R script execution
- `git` for version control

## Verification

After installation, verify that rxiv-maker is working correctly:

```bash
# Check version
rxiv --version

# Validate installation
rxiv check-installation

# Create test manuscript
rxiv init test-paper
cd test-paper
rxiv pdf
```

## Updating

To update to the latest version:

```bash
sudo apt update && sudo apt upgrade rxiv-maker
```

## Repository Details

- **Repository URL**: https://henriqueslab.github.io/rxiv-maker/
- **Distribution**: stable
- **Component**: main
- **Architectures**: amd64, arm64, all
- **GPG Key ID**: Available in the repository's `pubkey.gpg` file

## Alternative Installation Methods

If you prefer other installation methods:

### Direct .deb Download

```bash
# Download latest .deb package
wget https://github.com/henriqueslab/rxiv-maker/releases/latest/download/rxiv-maker_1.5.10-1_all.deb

# Install with dpkg
sudo dpkg -i rxiv-maker_*.deb

# Fix any dependency issues
sudo apt-get install -f
```

### PyPI Installation

```bash
pip install rxiv-maker
```

### Homebrew (macOS/Linux)

```bash
brew tap henriqueslab/rxiv-maker
brew install rxiv-maker
```

## Troubleshooting

### GPG Key Issues

If you encounter GPG key verification errors:

```bash
# Re-add the GPG key
curl -fsSL https://raw.githubusercontent.com/henriqueslab/rxiv-maker/apt-repo/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/rxiv-maker.gpg

# Update package lists
sudo apt update
```

### Repository Access Issues

If the repository is not accessible:

1. Check your internet connection
2. Verify the repository URL is correct
3. Try accessing https://henriqueslab.github.io/rxiv-maker/ in your browser

### Missing Dependencies

If some dependencies are missing after installation:

```bash
# Install missing LaTeX packages
sudo apt install texlive-full

# Install optional dependencies
sudo apt install docker.io nodejs npm r-base
```

### Permission Issues

If you encounter permission issues:

```bash
# Ensure user is in docker group (if using Docker)
sudo usermod -aG docker $USER
newgrp docker

# Fix potential cache permissions
sudo chown -R $USER:$USER ~/.cache/rxiv-maker
```

## Repository Maintenance

The APT repository is automatically updated when new versions of rxiv-maker are released. The repository includes:

- Signed packages for security
- Automatic metadata updates
- Version history and changelogs
- Installation verification

For the latest packages and updates, visit:
- Repository: https://henriqueslab.github.io/rxiv-maker/
- Releases: https://github.com/henriqueslab/rxiv-maker/releases
- Documentation: https://github.com/henriqueslab/rxiv-maker#readme