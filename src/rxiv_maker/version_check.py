"""Version checking utilities for rxiv-maker dependencies."""

import sys
import warnings
from importlib import import_module
from packaging import version
from typing import Dict, List, Optional, Tuple


# Minimum version requirements
MIN_VERSIONS = {
    'matplotlib': '3.6.0',
    'seaborn': '0.12.0', 
    'numpy': '1.24.0',
    'pandas': '2.0.0',
    'PIL': '9.0.0',  # Pillow
    'pypdf': '4.0.0',
    'yaml': '6.0.0',  # PyYAML
    'dotenv': '1.0.0',  # python-dotenv
    'click': '8.0.0',
    'rich': '13.0.0',
    'requests': '2.28.0',
    'packaging': '21.0.0',
    'platformdirs': '4.0.0',
    'typing_extensions': '4.0.0',
}

# Package name mappings (import name -> package name)
PACKAGE_MAPPINGS = {
    'PIL': 'Pillow',
    'yaml': 'PyYAML',
    'dotenv': 'python-dotenv',
}


def get_package_version(package_name: str) -> Optional[str]:
    """Get the installed version of a package."""
    try:
        module = import_module(package_name)
        # Try different common version attribute names
        for attr in ['__version__', 'version', 'VERSION']:
            if hasattr(module, attr):
                ver = getattr(module, attr)
                return str(ver)
        return None
    except ImportError:
        return None


def check_version_compatibility(package_name: str, required_version: str) -> Tuple[bool, Optional[str]]:
    """Check if installed package version meets minimum requirements."""
    installed_version = get_package_version(package_name)
    
    if installed_version is None:
        return False, None
    
    try:
        return version.parse(installed_version) >= version.parse(required_version), installed_version
    except Exception:
        # If version parsing fails, assume it's compatible
        return True, installed_version


def check_all_dependencies(warn_on_issues: bool = True) -> Dict[str, Tuple[bool, Optional[str], str]]:
    """
    Check all dependencies and their versions.
    
    Returns:
        Dict mapping package names to (is_compatible, installed_version, required_version)
    """
    results = {}
    issues = []
    
    for package, required_ver in MIN_VERSIONS.items():
        is_compatible, installed_ver = check_version_compatibility(package, required_ver)
        results[package] = (is_compatible, installed_ver, required_ver)
        
        if not is_compatible:
            display_name = PACKAGE_MAPPINGS.get(package, package)
            if installed_ver is None:
                issues.append(f"Missing package: {display_name}")
            else:
                issues.append(f"Outdated {display_name}: {installed_ver} < {required_ver}")
    
    if issues and warn_on_issues:
        warnings.warn(
            f"Dependency issues detected:\n" + "\n".join(f"  - {issue}" for issue in issues) +
            f"\n\nSome features may not work properly. " +
            f"Consider upgrading: pip install --upgrade {' '.join(PACKAGE_MAPPINGS.get(pkg, pkg) for pkg, (compat, _, _) in results.items() if not compat)}",
            UserWarning
        )
    
    return results


def validate_critical_dependencies() -> None:
    """Validate critical dependencies and exit if any are missing."""
    critical_packages = ['click', 'rich', 'requests']
    
    missing = []
    for package in critical_packages:
        if get_package_version(package) is None:
            missing.append(PACKAGE_MAPPINGS.get(package, package))
    
    if missing:
        print(f"❌ Critical dependencies missing: {', '.join(missing)}", file=sys.stderr)
        print("Please install them with: pip install " + " ".join(missing), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # Command-line version check utility
    print("Checking rxiv-maker dependencies...")
    results = check_all_dependencies(warn_on_issues=False)
    
    print("\nDependency Status:")
    for package, (is_compatible, installed_ver, required_ver) in results.items():
        display_name = PACKAGE_MAPPINGS.get(package, package)
        status = "✅" if is_compatible else ("❌" if installed_ver is None else "⚠️")
        installed_str = installed_ver or "not installed"
        print(f"  {status} {display_name:20} {installed_str:15} (required: {required_ver})")
    
    compatible_count = sum(1 for is_compat, _, _ in results.values() if is_compat)
    total_count = len(results)
    
    print(f"\nCompatibility: {compatible_count}/{total_count} packages meet requirements")
    
    if compatible_count < total_count:
        sys.exit(1)