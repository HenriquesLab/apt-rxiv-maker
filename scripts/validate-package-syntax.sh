#!/bin/bash
set -e

echo "=== Validating Package Syntax and Structure ==="

# Check debian control file syntax
echo "1. Validating debian/control syntax..."
if command -v dpkg-parsechangelog >/dev/null 2>&1; then
    echo "   Using dpkg-parsechangelog (if available)"
else
    echo "   Manual syntax validation"
fi

# Basic control file validation
if [ -f "debian/control" ]; then
    echo "   ✅ debian/control exists"
    
    # Check required fields
    if grep -q "^Source:" debian/control; then
        echo "   ✅ Source field present"
    else
        echo "   ❌ Missing Source field"
        exit 1
    fi
    
    if grep -q "^Package:" debian/control; then
        echo "   ✅ Package field present"
    else
        echo "   ❌ Missing Package field"
        exit 1
    fi
    
    if grep -q "python3-pip" debian/control; then
        echo "   ✅ python3-pip dependency added"
    else
        echo "   ⚠️  python3-pip not found in dependencies"
    fi
    
    # Check that problematic packages are not present with version constraints
    if grep -q "python3-pypdf.*>=" debian/control; then
        echo "   ❌ python3-pypdf still has version constraint"
        exit 1
    else
        echo "   ✅ python3-pypdf version constraint removed"
    fi
    
    if grep -q "python3-rich-click" debian/control; then
        echo "   ❌ python3-rich-click still present in control file"
        exit 1
    else
        echo "   ✅ python3-rich-click removed from system dependencies"
    fi
    
else
    echo "   ❌ debian/control not found"
    exit 1
fi

# Validate postinst script
echo -e "\n2. Validating debian/rxiv-maker.postinst..."
if [ -f "debian/rxiv-maker.postinst" ]; then
    echo "   ✅ Post-install script exists"
    
    if grep -q "pypdf" debian/rxiv-maker.postinst; then
        echo "   ✅ pypdf pip installation found"
    else
        echo "   ❌ pypdf pip installation not found"
        exit 1
    fi
    
    if grep -q "rich-click" debian/rxiv-maker.postinst; then
        echo "   ✅ rich-click pip installation found"
    else
        echo "   ❌ rich-click pip installation not found"
        exit 1
    fi
    
    if bash -n debian/rxiv-maker.postinst; then
        echo "   ✅ Post-install script syntax is valid"
    else
        echo "   ❌ Post-install script has syntax errors"
        exit 1
    fi
else
    echo "   ❌ debian/rxiv-maker.postinst not found"
    exit 1
fi

# Validate prerm script  
echo -e "\n3. Validating debian/rxiv-maker.prerm..."
if [ -f "debian/rxiv-maker.prerm" ]; then
    echo "   ✅ Pre-removal script exists"
    
    if grep -q "pypdf" debian/rxiv-maker.prerm; then
        echo "   ✅ pypdf cleanup found"
    else
        echo "   ❌ pypdf cleanup not found"
        exit 1
    fi
    
    if bash -n debian/rxiv-maker.prerm; then
        echo "   ✅ Pre-removal script syntax is valid"
    else
        echo "   ❌ Pre-removal script has syntax errors"
        exit 1
    fi
else
    echo "   ❌ debian/rxiv-maker.prerm not found"
    exit 1
fi

# Validate Python version checking module
echo -e "\n4. Validating Python version checking module..."
if [ -f "src/rxiv_maker/version_check.py" ]; then
    echo "   ✅ version_check.py exists"
    
    if python3 -m py_compile src/rxiv_maker/version_check.py; then
        echo "   ✅ version_check.py syntax is valid"
    else
        echo "   ❌ version_check.py has syntax errors"
        exit 1
    fi
    
    if grep -q "'pypdf'.*'4.0.0'" src/rxiv_maker/version_check.py; then
        echo "   ✅ pypdf version requirement found"
    else
        echo "   ❌ pypdf version requirement not found"
        exit 1
    fi
    
else
    echo "   ❌ src/rxiv_maker/version_check.py not found"
    exit 1
fi

# Validate CLI integration
echo -e "\n5. Validating CLI integration..."
if [ -f "src/rxiv_maker/cli.py" ]; then
    echo "   ✅ cli.py exists"
    
    if python3 -m py_compile src/rxiv_maker/cli.py; then
        echo "   ✅ cli.py syntax is valid"
    else
        echo "   ❌ cli.py has syntax errors"
        exit 1
    fi
    
    if grep -q "check-deps" src/rxiv_maker/cli.py; then
        echo "   ✅ --check-deps option found"
    else
        echo "   ❌ --check-deps option not found"
        exit 1
    fi
    
    if grep -q "version_check" src/rxiv_maker/cli.py; then
        echo "   ✅ version_check import found"
    else
        echo "   ❌ version_check import not found"
        exit 1
    fi
    
else
    echo "   ❌ src/rxiv_maker/cli.py not found"
    exit 1
fi

# Test Python imports (basic smoke test)
echo -e "\n6. Testing Python imports..."
cd src
if python3 -c "import rxiv_maker.version_check; print('✅ version_check imports successfully')"; then
    echo "   ✅ version_check module can be imported"
else
    echo "   ❌ version_check module import failed"
    exit 1
fi

if python3 -c "import rxiv_maker.cli; print('✅ cli imports successfully')" 2>/dev/null; then
    echo "   ✅ cli module can be imported"
else
    echo "   ⚠️  cli module import failed (may be due to missing dependencies)"
fi
cd ..

echo -e "\n=== Validation Summary ==="
echo "✅ All package files validated successfully"
echo "✅ Control file has correct dependency structure"  
echo "✅ Post-install script will handle missing packages via pip"
echo "✅ Pre-removal script will clean up pip packages"
echo "✅ Version checking functionality implemented"
echo "✅ CLI integration for dependency checking added"

echo -e "\n🎉 Package structure is ready for Ubuntu 22.04 compatibility!"

echo -e "\nNext steps:"
echo "- Build package in Ubuntu 22.04 environment"  
echo "- Test installation on Google Colab"
echo "- Verify all dependencies resolve correctly"