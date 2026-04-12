#!/bin/bash
set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

INSTALL_DIR="$HOME/.local/share/arch-rpc"
VENV_DIR="$INSTALL_DIR/venv"

echo -e "${BLUE}==>${NC} Checking dependencies..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}==>${NC} Python 3 not found. Please install Python first."
    exit 1
fi

if ! command -v notify-send &> /dev/null; then
    echo -e "${BLUE}==>${NC} libnotify not found. Installing..."
    sudo pacman -S --noconfirm libnotify
else
    echo -e "${GREEN}==>${NC} libnotify is already installed."
fi

echo -e "${BLUE}==>${NC} Stopping old service if running..."
systemctl --user stop arch-rpc.service 2>/dev/null || true

echo -e "${BLUE}==>${NC} Installing files to $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
cp main.py setup.py requirements.txt "$INSTALL_DIR/"

echo -e "${BLUE}==>${NC} Creating virtual environment..."
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install -r "$INSTALL_DIR/requirements.txt" --quiet

echo -e "${BLUE}==>${NC} Setting up autostart (systemd) and shortcuts..."
"$VENV_DIR/bin/python" "$INSTALL_DIR/setup.py"

echo -e "${GREEN}==>${NC} Installation complete!"
echo -e "${GREEN}==>${NC} Check logs with: journalctl --user -u arch-rpc.service -f"