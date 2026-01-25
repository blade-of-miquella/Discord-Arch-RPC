import time
import sys, os, signal, subprocess
from pypresence import Presence, DiscordNotFound

CLIENT_ID = '1460668472647356499'

paused = False
last_signal_time = 0

def toggle_pause(sig, frame) -> None:
    global paused, last_signal_time
    
    current_time = time.time()
    if current_time - last_signal_time < 1.0:
        return
    
    last_signal_time = current_time
    paused = not paused
    
    subprocess.run(["notify-send", "Arch RPC", 
                    f"Status {'Paused' if paused else 'Resumed'}", 
                    "-i", "discord", "-h", "string:x-canonical-private-synchronous:rpc-notif"])

signal.signal(signal.SIGUSR1, toggle_pause)

def main() -> None:
    global paused
    
    current_pid = os.getpid()
    output = subprocess.check_output(["pgrep", "-f", "arch-rpc"]).decode()
    for pid in output.split():
        if int(pid) != current_pid:
            os.kill(int(pid), signal.SIGKILL)

    while True:
        try:
            rpc = Presence(CLIENT_ID)
            rpc.connect()
            start_time = time.time()

            while True:
                if not paused:
                    rpc.update(
                        details="using Arch btw",
                        large_image="arch_logo",
                        large_text="Arch Linux",
                        start=start_time
                    )
                else:
                    rpc.clear()

                for _ in range(15):
                    time.sleep(1)
                    if paused:
                        rpc.clear()
                    if not paused and _ > 0: 
                        break
        except:
            time.sleep(20)

if __name__ == "__main__":
    main()