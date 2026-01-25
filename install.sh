#!/bin/bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}==>${NC} Checking dependencies..."

if ! command -v notify-send &> /dev/null; then
    echo -e "${BLUE}==>${NC} libnotify not found. Installing..."
    sudo pacman -S --noconfirm libnotify
else
    echo -e "${GREEN}==>${NC} libnotify is already installed."
fi

echo -e "${BLUE}==>${NC} Building Arch RPC..."

python -m venv temp_venv
source temp_venv/bin/activate
pip install pypresence pyinstaller --quiet

echo -e "${BLUE}==>${NC} Compiling..."
pyinstaller --onefile --name arch-rpc "main.py" --log-level ERROR
pyinstaller --onefile --name arch-setup "setup.py" --log-level ERROR

echo -e "${BLUE}==>${NC} Installing binaries to ~/.local/bin..."
mkdir -p "$HOME/.local/bin"
cp "dist/arch-rpc" "$HOME/.local/bin/"
cp "dist/arch-setup" "$HOME/.local/bin/"

echo -e "${BLUE}==>${NC} Setup autostart and shortcuts..."
"$HOME/.local/bin/arch-setup"

echo -e "${BLUE}==>${NC} Clearing trash..."
deactivate
rm -rf temp_venv build dist arch-rpc.spec arch-setup.spec

echo -e "${GREEN}==>${NC} Completed! App located in ~/.local/bin/"

"$HOME/.local/bin/arch-rpc" &