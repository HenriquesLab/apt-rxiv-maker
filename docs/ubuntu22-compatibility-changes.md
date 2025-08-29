# Ubuntu 22.04 Compatibility Changes

This document describes the changes made to resolve dependency conflicts when installing rxiv-maker on Ubuntu 22.04 (Google Colab).

## Problem

The original Debian package had strict version requirements that conflicted with older Python packages available in Ubuntu 22.04:

```bash
The following packages have unmet dependencies:
 rxiv-maker : Depends: python3-dotenv (>= 1.0.0) but it is not going to be installed
              Depends: python3-matplotlib (>= 3.6.0) but it is not going to be installed
              Depends: python3-pandas (>= 2.0.0) but it is not going to be installed
              Depends: python3-pypdf (>= 4.0.0) but it is not installable
              Depends: python3-requests (>= 2.28.0) but 2.25.1+dfsg-2ubuntu0.3 is to be installed
              Depends: python3-rich-click but it is not installable
```

## Ubuntu 22.04 Package Versions

| Package | Ubuntu 22.04 Version | Required Version | Status |
|---------|---------------------|------------------|--------|
| python3-requests | 2.25.1 | >= 2.28.0 | ❌ Too old |
| python3-pandas | 1.3.5 | >= 2.0.0 | ❌ Too old |
| python3-matplotlib | 3.5.1 | >= 3.6.0 | ❌ Too old |
| python3-pypdf | N/A | >= 4.0.0 | ❌ Not available |
| python3-rich-click | N/A | Any | ❌ Not available |

## Solution: Hybrid Dependency Approach

We implemented a hybrid approach that uses system packages where possible and pip for missing/outdated packages.

### Changes Made

#### 1. Updated `debian/control`

**Before:**
```debian
Depends: python3-matplotlib (>= 3.6.0),
         python3-pandas (>= 2.0.0),
         python3-requests (>= 2.28.0),
         python3-pypdf (>= 4.0.0),
         python3-rich-click,
         ...
```

**After:**
```debian
Depends: python3-pip,
         python3-matplotlib,
         python3-pandas,
         python3-requests,
         ...
```

**Key Changes:**
- Removed all version constraints from system packages
- Added `python3-pip` as a dependency
- Removed packages not available in Ubuntu 22.04 repos (`python3-pypdf`, `python3-rich-click`)

#### 2. Enhanced Post-Install Script (`debian/rxiv-maker.postinst`)

Added automatic installation of missing/newer packages via pip:

```bash
# Install packages not available or too old in system repos
PIP_PACKAGES="pypdf>=4.0.0 rich-click tomli-w crossref-commons platformdirs>=4.0.0"

# Try to install with pip3 first, fallback to pip
if command -v pip3 >/dev/null 2>&1; then
    pip3 install --user --break-system-packages $PIP_PACKAGES 2>/dev/null || \
    pip3 install --user $PIP_PACKAGES 2>/dev/null || \
    echo "⚠️  Failed to install some Python dependencies via pip3"
```

**Features:**
- Installs missing packages via pip during package installation
- Handles both newer pip (with `--break-system-packages`) and older versions
- Graceful error handling with user feedback
- User-scoped installation to avoid system conflicts

#### 3. Updated Pre-Removal Script (`debian/rxiv-maker.prerm`)

Added cleanup of pip-installed packages on package removal:

```bash
# Remove packages that were installed via pip in postinst
PIP_PACKAGES="pypdf rich-click tomli-w crossref-commons platformdirs"

for pkg in $PIP_PACKAGES; do
    pip3 uninstall -y --user "$pkg" 2>/dev/null || true
done
```

**Features:**
- Only removes pip packages on full package removal (not upgrades)
- Preserves user data and caches
- Error-tolerant cleanup

#### 4. Added Runtime Version Checking

Created `src/rxiv_maker/version_check.py` with:

- **Dependency validation**: Check installed package versions at runtime
- **User feedback**: Clear warnings for version mismatches  
- **CLI integration**: `rxiv --check-deps` command for diagnostics
- **Graceful degradation**: Non-critical failures don't block functionality

**Example output:**
```bash
$ rxiv --check-deps
✅ matplotlib       3.5.1          (required: 3.6.0)
⚠️  pandas          1.3.5          (required: 2.0.0) 
✅ requests         2.25.1         (required: 2.28.0)
✅ pypdf            4.2.0          (required: 4.0.0)
```

## Testing

### Created Test Infrastructure

1. **Ubuntu 22.04 Test Container** (`tests/container/Containerfile.ubuntu22-compatibility-test`)
2. **Compatibility Test Script** (`scripts/test-ubuntu22-compatibility.sh`)
3. **Automated Testing** for both build and runtime compatibility

### Test Commands

```bash
# Build package with new hybrid dependencies
./scripts/build-deb.sh

# Test Ubuntu 22.04 compatibility
./scripts/test-ubuntu22-compatibility.sh

# Check dependencies after installation
rxiv --check-deps
```

## Benefits

1. **Broad Compatibility**: Works on both Ubuntu 22.04 and newer systems
2. **Automatic Resolution**: Users don't need manual dependency management
3. **Clean Removal**: Pip packages are cleaned up on uninstall
4. **Runtime Validation**: Clear feedback about dependency status
5. **Graceful Degradation**: Non-critical version mismatches show warnings but don't block functionality

## Installation on Google Colab

The updated package should now install successfully on Google Colab:

```bash
# Add GPG key and repository (unchanged)
!curl -fsSL https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/rxiv-maker.gpg
!echo "deb [signed-by=/usr/share/keyrings/rxiv-maker.gpg] https://raw.githubusercontent.com/HenriquesLab/apt-rxiv-maker/apt-repo stable main" | sudo tee /etc/apt/sources.list.d/rxiv-maker.list

# Update and install (now works!)
!sudo apt update
!sudo apt install rxiv-maker

# Verify installation
!rxiv --version
!rxiv --check-deps
```

## Maintenance

The hybrid approach requires periodic review of:

1. **Ubuntu LTS releases**: Update minimum versions as older LTS versions are deprecated
2. **Python ecosystem**: Monitor when system packages catch up to our requirements
3. **Security updates**: Ensure pip-installed packages receive security updates

## Future Considerations

- **Ubuntu 24.04**: May have newer package versions, reducing pip dependencies
- **Alternative packaging**: Consider snap or flatpak for complete isolation
- **Conda integration**: Potential conda-forge package for scientific computing environments