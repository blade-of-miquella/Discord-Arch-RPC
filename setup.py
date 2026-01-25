import os

def autostart():
    exe_path = os.path.expanduser("~/.local/bin/arch-rpc")
    
    # Check for hyprland
    is_hyprland = os.environ.get('HYPRLAND_INSTANCE_SIGNATURE') is not None

    if is_hyprland:
        config_path = os.path.expanduser("~/.config/hypr/hyprland.conf")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                content = f.read()
            
            if exe_path not in content:
                with open(config_path, 'a') as f:
                    f.write(f"\n# Discord RPC Presence\nexec-once = {exe_path}\n")
                print("Added autostart to hyprland.conf")
            else:
                print("Autostart already in hyprland.conf")

            shortcut_cmd = "bind = $mainMod SHIFT, P, exec, pkill -USR1 arch-rpc"
            if "pkill -USR1 arch-rpc" not in content:
                with open(config_path, 'a') as f:
                    f.write(f"{shortcut_cmd}\n")
                print("Added shortcut (Super+Shift+P) to hyprland.conf")
            else:
                print("Shortcut already in hyprland.conf")

    else:
        # For other DE using .desktop
        autostart_path = os.path.expanduser("~/.config/autostart")
        os.makedirs(autostart_path, exist_ok=True)

        desktop_file = f"""[Desktop Entry]
            Type=Application
            Exec={exe_path}
            Hidden=false
            NoDisplay=false
            X-GNOME-Autostart-enabled=true
            Name=ArchRPC
            Comment=Discord Rich Presence
            """

        with open(os.path.join(autostart_path, "arch-rpc.desktop"), "w") as f:
            f.write(desktop_file)
        print("Created .desktop file in ~/.config/autostart")
        
        print("\nNOTE: For non-Hyprland environments, please set your global shortcut")
        print("manually to run this command: pkill -USR1 arch-rpc")

if __name__ == "__main__":
    autostart()