import os

exe_path = os.path.expanduser("~/.local/bin/arch-rpc")
is_hyprland = os.environ.get('HYPRLAND_INSTANCE_SIGNATURE') is not None

if is_hyprland:
    config_path = os.path.expanduser("~/.config/hypr/hyprland.conf")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            content = f.read()
        
        changed = False
        if exe_path not in content:
            with open(config_path, 'a') as f:
                f.write(f"\nexec-once = {exe_path}\n")
            changed = True
        if "pkill -USR1 arch-rpc" not in content:
            with open(config_path, 'a') as f:
                f.write("bind = $mainMod SHIFT, P, exec, pkill -USR1 arch-rpc\n")
            changed = True
        
    else:
        pass
else:
    path = os.path.expanduser("~/.config/autostart/arch-rpc.desktop")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(f"""[Desktop Entry]
            Type=Application
            Exec={exe_path}
            Hidden=false
            NoDisplay=false
            X-GNOME-Autostart-enabled=true
            Name=ArchRPC
            Comment=Discord Rich Presence""")