#!/bin/bash
set -e

# Speed up Python installs
export PIP_NO_CACHE_DIR=1
export PYTHONUNBUFFERED=1

# Install dependencies with parallel processing
pip install --upgrade pip
pip install --use-pep517 --extra-index-url https://pypi.anaconda.org/scientific-python-nightly-wheels/simple -r requirements.txt

# Create minimal build output
mkdir -p public
echo "<!DOCTYPE html><html><body>Flask app is running</body></html>" > public/index.html