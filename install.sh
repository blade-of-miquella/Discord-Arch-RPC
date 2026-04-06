#!/bin/bash
set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

cleanup() {
    echo -e "${BLUE}==>${NC} Cleaning up temporary files..."
    deactivate 2>/dev/null || true
    rm -rf temp_venv build dist arch-rpc.spec arch-setup.spec
}
trap cleanup EXIT

echo -e "${BLUE}==>${NC} Checking dependencies..."

if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo -e "${RED}==>${NC} Python not found. Please install Python first."
    exit 1
fi

PYTHON=$(command -v python3 || command -v python)

if ! command -v notify-send &> /dev/null; then
    echo -e "${BLUE}==>${NC} libnotify not found. Installing..."
    sudo pacman -S --noconfirm libnotify
else
    echo -e "${GREEN}==>${NC} libnotify is already installed."
fi

echo -e "${BLUE}==>${NC} Building Arch RPC..."

"$PYTHON" -m venv temp_venv
source temp_venv/bin/activate
pip install -r requirements.txt --quiet

echo -e "${BLUE}==>${NC} Compiling..."
pyinstaller --onefile --name arch-rpc "main.py" --log-level ERROR
pyinstaller --onefile --name arch-setup "setup.py" --log-level ERROR

echo -e "${BLUE}==>${NC} Stopping old service if running..."
systemctl --user stop arch-rpc.service 2>/dev/null || true

echo -e "${BLUE}==>${NC} Installing binaries to ~/.local/bin..."
mkdir -p "$HOME/.local/bin"
cp "dist/arch-rpc" "$HOME/.local/bin/"
cp "dist/arch-setup" "$HOME/.local/bin/"

echo -e "${BLUE}==>${NC} Setup autostart (systemd) and shortcuts..."
"$HOME/.local/bin/arch-setup"

echo -e "${GREEN}==>${NC} Installation complete!"
echo -e "${GREEN}==>${NC} Check logs with: journalctl --user -u arch-rpc.service -f"