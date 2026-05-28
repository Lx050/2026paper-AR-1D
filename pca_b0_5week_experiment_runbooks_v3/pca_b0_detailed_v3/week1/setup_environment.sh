#!/usr/bin/env bash
set -euo pipefail
conda create -n pca-b0 python=3.10 -y
conda activate pca-b0
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/pca_b0_smoke_test.py
