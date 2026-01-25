import time
import sys
from pypresence import Presence, DiscordNotFound

CLIENT_ID = '1460668472647356499'

def main() -> None:
    print("Starting Arch RPC...")
    
    while True:
        try:
            rpc = Presence(CLIENT_ID)
            rpc.connect()
            print("Connected to Discord!")

            start_time = time.time()

            while True:
                rpc.update(
                    details="using Arch btw",
                    large_image="arch_logo",
                    large_text="Arch Linux",
                    start=start_time
                )
                time.sleep(15)
                
        except (DiscordNotFound, ConnectionResetError, Exception) as e:
            time.sleep(20)
            continue

if __name__ == "__main__":
    main()