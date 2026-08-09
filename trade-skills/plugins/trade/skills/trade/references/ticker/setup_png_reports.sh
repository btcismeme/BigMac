#!/bin/bash
# Setup script for PNG report generation feature
# Installs required dependencies for generating Chinese-language trading reports

set -e

echo "📦 Setting up PNG Report Generation..."
echo ""

# Check Python version
python_cmd=$(which python3 || which python)
if [ -z "$python_cmd" ]; then
    echo "❌ Error: Python not found. Please install Python 3.7+"
    exit 1
fi

echo "✓ Python found: $python_cmd"
python_version=$($python_cmd --version)
echo "  Version: $python_version"
echo ""

# Install Pillow
echo "📥 Installing Pillow (image generation library)..."
$python_cmd -m pip install --upgrade Pillow

if $python_cmd -c "import PIL" 2>/dev/null; then
    pil_version=$($python_cmd -c "import PIL; print(PIL.__version__)")
    echo "✓ Pillow installed successfully (version: $pil_version)"
else
    echo "❌ Failed to install Pillow"
    exit 1
fi

echo ""
echo "✅ Setup complete! You can now generate PNG reports."
echo ""
echo "Usage:"
echo "  cd $(dirname "$0")"
echo "  python3 generate_png_report.py          # Generate default MU report"
echo "  python3 generate_png_report.py MU       # Generate MU report"
echo ""
echo "For more information, see README_PNG_REPORTS.md"
