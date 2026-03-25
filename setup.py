import os
import subprocess

exe_path = os.path.expanduser("~/.local/bin/arch-rpc")

def setup_systemd():
    service_content = f"""[Unit]
        Description=Discord Arch RPC
        After=network.target

        [Service]
        Type=simple
        ExecStart={exe_path}
        Restart=always
        RestartSec=10
        Environment=PYTHONUNBUFFERED=1

        [Install]
        WantedBy=default.target
        """
    
    systemd_dir = os.path.expanduser("~/.config/systemd/user")
    os.makedirs(systemd_dir, exist_ok=True)
    
    service_path = os.path.join(systemd_dir, "arch-rpc.service")
    with open(service_path, "w") as f:
        f.write(service_content)
        
    subprocess.run(["systemctl", "--user", "daemon-reload"])
    subprocess.run(["systemctl", "--user", "enable", "--now", "arch-rpc.service"])

def setup_hyprland_bind():
    is_hyprland = os.environ.get('HYPRLAND_INSTANCE_SIGNATURE') is not None
    if not is_hyprland:
        return
        
    config_path = os.path.expanduser("~/.config/hypr/hyprland.conf")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            content = f.read()
        
        if "pkill -USR1 arch-rpc" not in content:
            with open(config_path, 'a') as f:
                f.write("\n# Arch-RPC Pause Bind\n")
                f.write("bind = $mainMod SHIFT, P, exec, pkill -USR1 arch-rpc\n")

if __name__ == "__main__":
    setup_systemd()
    setup_hyprland_bind()