import time
import signal
import subprocess
from pypresence import Presence, DiscordNotFound

CLIENT_ID = '1460668472647356499'
paused = False
last_signal_time = 0
interrupt_sleep = False

def toggle_pause(sig, frame):
    global paused, last_signal_time, interrupt_sleep
    current_time = time.time()
    
    if current_time - last_signal_time < 1:
        return
    last_signal_time = current_time
    
    paused = not paused
    interrupt_sleep = True
    
    status = "Paused" if paused else "Continued"
    subprocess.Popen(["notify-send", "Arch RPC", f"Status: {status}", "-i", "discord", "-h", "string:x-canonical-private-synchronous:rpc-notif"])

def smart_sleep(seconds):
    global interrupt_sleep
    interrupt_sleep = False
    for _ in range(int(seconds)):
        if interrupt_sleep:
            break
        time.sleep(1)

def main():
    signal.signal(signal.SIGUSR1, toggle_pause)

    while True:
        rpc = None
        try:
            rpc = Presence(CLIENT_ID)
            rpc.connect()
            start_time = int(time.time())

            while True:
                if not paused:
                    rpc.update(details="using Arch btw", large_image="arch_logo", large_text="Arch Linux", start=start_time)
                else:
                    rpc.clear()
                
                smart_sleep(15)
                
        except (DiscordNotFound, ConnectionRefusedError):
            time.sleep(15)
        except Exception as e:
            time.sleep(15)
        finally:
            if rpc:
                try: rpc.close()
                except: pass
                del rpc 

if __name__ == "__main__":
    main()