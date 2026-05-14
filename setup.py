import os
import shutil
import logging
import subprocess
import textwrap

INSTALL_DIR = os.path.expanduser("~/.local/share/arch-rpc")
venv_python = os.path.join(INSTALL_DIR, "venv", "bin", "python")
script_path = os.path.join(INSTALL_DIR, "main.py")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger(__name__)

def setup_systemd():
    service_content = textwrap.dedent(f"""\
        [Unit]
        Description=Discord Arch RPC
        After=network.target

        [Service]
        Type=simple
        ExecStart={venv_python} {script_path}
        Restart=always
        RestartSec=10
        Environment=PYTHONUNBUFFERED=1

        [Install]
        WantedBy=default.target
        """)

    systemd_dir = os.path.expanduser("~/.config/systemd/user")
    os.makedirs(systemd_dir, exist_ok=True)

    service_path = os.path.join(systemd_dir, "arch-rpc.service")
    with open(service_path, "w") as f:
        f.write(service_content)

    subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "--user", "enable", "--now", "arch-rpc.service"], check=True)
    logger.info("systemd service enabled and started.")

def setup_hyprland_bind():
    is_hyprland = os.environ.get('HYPRLAND_INSTANCE_SIGNATURE') is not None
    if not is_hyprland:
        return

    config_path = os.path.expanduser("~/.config/hypr/hyprland.lua")
    if not os.path.exists(config_path):
        return

    with open(config_path, 'r') as f:
        content = f.read()

    bind_cmd = "systemctl --user kill -s USR1 arch-rpc.service"
    if bind_cmd not in content:
        backup_path = config_path + ".bak"
        shutil.copy2(config_path, backup_path)
        logger.info("Backed up hyprland.conf to %s", backup_path)

        with open(config_path, 'a') as f:
            f.write(f'hl.bind("SUPER" .. " + SHIFT + P", hl.dsp.exec_cmd("{bind_cmd}"))')
        logger.info("Added Hyprland key binding.")

if __name__ == "__main__":
    setup_systemd()
    setup_hyprland_bind()
