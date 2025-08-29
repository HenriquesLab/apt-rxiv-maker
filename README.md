# Rxiv-Maker APT Repository

This repository contains Debian packages for rxiv-maker.

## Usage

Add this repository to your system:

```bash
# Add GPG key
curl -fsSL https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/rxiv-maker.gpg

# Add repository
echo "deb [signed-by=/usr/share/keyrings/rxiv-maker.gpg] https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo stable main" | sudo tee /etc/apt/sources.list.d/rxiv-maker.list

# Update package list
sudo apt update

# Install rxiv-maker
sudo apt install rxiv-maker
```

## Packages

- `rxiv-maker` - Main package with all dependencies
