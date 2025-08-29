#!/bin/bash
set -e

echo "=== Testing Ubuntu 22.04 Compatibility ==="

# Build the new package with hybrid dependencies
echo "Building package with updated dependencies..."
./scripts/build-deb.sh

# Check if package was built
if [ ! -f *.deb ]; then
    echo "❌ Package build failed - no .deb file found"
    exit 1
fi

DEB_FILE=$(ls -1 *.deb | head -1)
echo "✅ Package built: $DEB_FILE"

# Test with Ubuntu 22.04 container
echo "Testing installation in Ubuntu 22.04 container..."

# Create a temporary test script
cat > /tmp/test-install.sh << 'EOF'
#!/bin/bash
set -e

echo "=== Ubuntu Version ==="
cat /etc/os-release | grep -E "(NAME|VERSION)"

echo -e "\n=== Installing Dependencies ==="
apt-get update
apt-get install -y python3 python3-pip curl

echo -e "\n=== Installing Package ==="
dpkg -i /package/*.deb || true
apt-get install -f -y  # Fix dependencies if needed

echo -e "\n=== Testing Installation ==="
if command -v rxiv >/dev/null 2>&1; then
    echo "✅ rxiv command available"
    rxiv --version
    echo -e "\n=== Checking Dependencies ==="
    rxiv --check-deps
else
    echo "❌ rxiv command not found"
    exit 1
fi

echo -e "\n=== Python Package Versions ==="
python3 -c "
import sys
packages = ['matplotlib', 'pandas', 'requests', 'numpy']
for pkg in packages:
    try:
        module = __import__(pkg)
        version = getattr(module, '__version__', 'unknown')
        print(f'{pkg:12}: {version}')
    except ImportError:
        print(f'{pkg:12}: not installed')
"

echo -e "\n=== Test Complete ==="
EOF

chmod +x /tmp/test-install.sh

# Run the test in Ubuntu 22.04 container
if command -v podman >/dev/null 2>&1; then
    RUNTIME=podman
elif command -v docker >/dev/null 2>&1; then
    RUNTIME=docker
else
    echo "❌ Neither podman nor docker found"
    exit 1
fi

echo "Using container runtime: $RUNTIME"

# Clean up any existing test containers
$RUNTIME rm -f rxiv-test-ubuntu22 2>/dev/null || true

# Create directory structure for bind mount
mkdir -p /tmp/rxiv-test-package
cp "$DEB_FILE" /tmp/rxiv-test-package/

# Run the test
$RUNTIME run --name rxiv-test-ubuntu22 \
    --rm \
    -v /tmp/test-install.sh:/test-install.sh:ro \
    -v /tmp/rxiv-test-package:/package:ro \
    ubuntu:22.04 \
    bash /test-install.sh

echo "✅ Ubuntu 22.04 compatibility test completed successfully!"

# Cleanup
rm -f /tmp/test-install.sh
rm -rf /tmp/rxiv-test-package

echo "=== Test Summary ==="
echo "✅ Package builds successfully"
echo "✅ Installs on Ubuntu 22.04"
echo "✅ Dependencies resolved via hybrid approach"
echo "✅ Command line interface works"