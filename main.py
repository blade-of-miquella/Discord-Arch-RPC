import time
import signal
import logging
import subprocess
import threading
from pypresence import Presence, DiscordNotFound

CLIENT_ID = '1460668472647356499'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger(__name__)

paused = False
last_signal_time = 0
interrupt_event = threading.Event()

def toggle_pause(sig, frame):
    global paused, last_signal_time
    current_time = time.time()

    if current_time - last_signal_time < 1:
        return
    last_signal_time = current_time

    paused = not paused
    interrupt_event.set()

    status = "Paused" if paused else "Continued"
    logger.info("Status toggled: %s", status)
    subprocess.run(
        ["notify-send", "Arch RPC", f"Status: {status}", "-i", "discord",
         "-h", "string:x-canonical-private-synchronous:rpc-notif"],
        check=False,
    )

def smart_sleep(seconds):
    interrupt_event.clear()
    interrupt_event.wait(timeout=seconds)

def main():
    signal.signal(signal.SIGUSR1, toggle_pause)

    while True:
        rpc = None
        try:
            rpc = Presence(CLIENT_ID)
            rpc.connect()
            logger.info("Connected to Discord.")
            start_time = int(time.time())

            while True:
                if not paused:
                    rpc.update(
                        details="using Arch btw",
                        large_image="arch_logo",
                        large_text="Arch Linux",
                        start=start_time,
                    )
                else:
                    rpc.clear()

                smart_sleep(15)

        except (DiscordNotFound, ConnectionRefusedError):
            logger.warning("Discord not found or connection refused. Retrying in 15s...")
            time.sleep(15)
        except Exception as e:
            logger.exception("Unexpected error: %s", e)
            time.sleep(15)
        finally:
            if rpc:
                try:
                    rpc.close()
                except Exception:
                    logger.debug("Error while closing RPC connection.", exc_info=True)

if __name__ == "__main__":
    main()