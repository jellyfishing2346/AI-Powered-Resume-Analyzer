#!/bin/bash
set -ex

# Speed up pip (disable cache, parallel installs)
export PIP_NO_CACHE_DIR=1
export PIP_FIND_LINKS="https://pypi.anaconda.org/scientific-python-nightly-wheels/simple"
export PIP_EXTRA_INDEX_URL="https://pypi.anaconda.org/intel/simple"

# Install in two phases (core first, heavy deps second)
pip install --upgrade pip
pip install --use-pep517 -r <(grep -v 'numpy\|scikit-learn\|blis' requirements.txt)
pip install --use-pep517 -r <(grep 'numpy\|scikit-learn\|blis' requirements.txt)

# Minimal build output
mkdir -p public
echo "<!DOCTYPE html><html><body>Flask backend ready</body></html>" > public/index.html