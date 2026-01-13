#!/bin/bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}==>${NC} Building Arch RPC..."

python -m venv temp_venv
source temp_venv/bin/activate

pip install pypresence pyinstaller --quiet

echo -e "${BLUE}==>${NC} Compiling..."
pyinstaller --onefile --name arch-rpc main.py
pyinstaller --onefile --name arch-setup setup.py

mkdir -p "$HOME/.local/bin"
cp dist/arch-rpc "$HOME/.local/bin/"
cp dist/arch-setup "$HOME/.local/bin/"

echo -e "${BLUE}==>${NC} Setup autostart..."
"$HOME/.local/bin/arch-setup"

echo -e "${BLUE}==>${NC} Clearing trash..."
deactivate
rm -rf temp_venv build dist arch-rpc.spec arch-setup.spec

echo -e "${GREEN}==>${NC} Completed! App located in ~/.local/bin/"

"$HOME/.local/bin/arch-rpc" &