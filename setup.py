import os

def autostart():
    exe_path = os.path.expanduser("~/.local/bin/arch-rpc")

    #check for hypland
    is_hyprland = os.environ.get('HYPRLAND_INSTANCE_SIGNATURE') is not None

    if is_hyprland:
        config_path = os.path.expanduser("~/.config/hypr/hyprland.conf")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                content = f.read()
            if exe_path not in content:
                with open(config_path, 'a') as f:
                    f.write(f"\n# Discord RPC Presence\nexec-once = {exe_path}\n")
                print("Added to hyprland.conf")
            else:
                print("Already in")

    else:
        #for other DE using .desktop
        autostart_path = os.path.expanduser("~/.config/autostart")
        os.makedir(autostart_path, exist_ok=True)

        desktop_file = f"""[Desktop Entry]
            Type=Application
            Exec={exe_path}
            Hidden=false
            NoDisplay=false
            X-GNOME-Autostart-enabled=true
            Name=ArchRPC
            Comment=Discord Rich Presence
            """

        with open(f"{autostart_path}/arch-rpc.desktop", "w") as f:
            f.write(desktop_file)
        print("Created .desktop")

if __name__ == "__main__":
    autostart()