# Arch Linux Discord RPC

Shows "using arch btw" in your Discord status. 
Supports automatic startup for **Hyprland** and standard XDG environments (GNOME, KDE, etc).

## Shortcut

- Hyprland: The installer automatically adds a binding to your `hyprland.conf` (Default: `$mainMod + Shift + P`).
- Other Environments: You can manually set a shortcut to run the command: `pkill -USR1 arch-rpc`.

## Installation

Run the following commands in your terminal:

```bash
git clone https://github.com/blade-of-miquella/Discord-Arch-RPC.git
cd Discord-Arch-RPC
chmod +x install.sh
./install.sh
