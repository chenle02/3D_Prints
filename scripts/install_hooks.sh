#!/usr/bin/env bash
set -e
# Directory where we store our versioned hooks
HOOKS_DIR=.githooks
# Configure Git to use the versioned hooks directory
git config core.hooksPath ${HOOKS_DIR}
# Ensure our hook and helper script are executable
chmod +x ${HOOKS_DIR}/pre-commit
chmod +x scripts/generate_stl_previews.py
echo "Git hooks installed. Pre-commit will generate PNG previews for new STL files."