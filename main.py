import time
import os
import signal
import subprocess
from pypresence import Presence, DiscordNotFound

paused = False
last_signal_time = 0

def toggle_pause(sig, frame):
    global paused, last_signal_time
    current_time = time.time()
    if current_time - last_signal_time < 1.0:
        return
    last_signal_time = current_time
    paused = not paused
    status = "Paused" if paused else "Continued"
    subprocess.run(["notify-send", "Arch RPC", f"Status: {status}", "-i", "discord", "-h", "string:x-canonical-private-synchronous:rpc-notif"], timeout=3)

def kill_other_instances():
    current_pid = os.getpid()
    try:
        output = subprocess.check_output(["pgrep", "-f", "arch-rpc"]).decode().strip()
        for pid_str in output.splitlines():
            if int(pid_str) != current_pid:
                os.kill(int(pid_str), signal.SIGKILL)
    except:
        pass

def main():
    global paused
    kill_other_instances()
    signal.signal(signal.SIGUSR1, toggle_pause)

    while True:
        rpc = None
        try:
            rpc = Presence('1460668472647356499')
            rpc.connect()
            start_time = int(time.time())
            while True:
                try:
                    if not paused:
                        rpc.update(details="using Arch btw", large_image="arch_logo", large_text="Arch Linux", start=start_time)
                    else:
                        rpc.clear()
                    time.sleep(15)
                except:
                    break
        except DiscordNotFound:
            time.sleep(8)
        except:
            time.sleep(10)
        finally:
            if rpc:
                try:
                    rpc.close()
                except:
                    pass

if __name__ == "__main__":
    main()