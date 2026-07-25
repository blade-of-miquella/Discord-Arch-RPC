# Arch Linux Discord RPC

Shows "using arch btw" in your Discord status.
Supports automatic startup via **systemd** with optional **Hyprland** key binding.

> **Note:** Discord must be running before starting the service.

## Shortcut

- **Hyprland:** The installer automatically adds a key binding to your `hyprland.lua` (Default: `$mainMod + Shift + P`) to toggle pause.
- **Other WMs / manual control:**
  ```bash
  # Pause / resume
  pkill -USR1 arch-rpc

  # Stop the service
  systemctl --user stop arch-rpc.service

  # Start the service
  systemctl --user start arch-rpc.service

  # Check status
  systemctl --user status arch-rpc.service
  ```

## Installation

Run the following commands in your terminal:

```bash
git clone https://github.com/blade-of-miquella/Discord-Arch-RPC.git
cd Discord-Arch-RPC
chmod +x install.sh
./install.sh
```

## Logs

```bash
journalctl --user -u arch-rpc.service -f
```
