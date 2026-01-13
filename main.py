import time
import sys
from pypresence import Presence

CLIENT_ID = '1460668472647356499'

def main() -> None:
    try:
        rpc = Presence(CLIENT_ID)
        rpc.connect()

        start_time = time.time()

        while True:
            rpc.update(
                details="using Arch btw",
                large_image="arch_logo",
                large_text="Arch Linux",
                start=start_time
            )
            time.sleep(15)
    except Exception as e:
        time.sleep(20)
        main()

if __name__ == "__main__":
    main()