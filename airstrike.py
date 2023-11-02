from nsdotpy.session import NSSession, canonicalize
from getpass import getpass
import time

with open("banner.txt","r",encoding="utf8") as f:
    print(f.read())

# Get parameters
main = canonicalize(input("Your main nation: "))
session = NSSession("Airstrike","0.1","Volstrostia",main)

region = canonicalize(input("Region: ")) # TODO: Track from nation
nation = canonicalize(input("RO Nation: "))
password = getpass("Password: ")

banfile = input("Path to banlist: ")
# TODO: Integrate with scribe to determine case-by-case
ban = False if str(input("Eject only? (y/N) ")).lower().startswith("y") else True

if session.login(nation, password):
    # Read banlist
    nations = []
    with open(banfile, "r") as f:
        for line in f.readlines():
            nations.append(canonicalize(line.strip()))

    for nation in nations:
        fails = 0
        failure = False
        print(f"\r[*] AGM LOCK ON -[ {nation.upper()} ]-")

        if ban: 
            # Try to ban over and over, until ratelimit clears
            while not session.banject(nation):
                print(f"\r[!] Bomb bay doors stuck closed!")
                fails += 1
                if fails > 3:
                    print(f"\r[!] Three strikes and {nation.upper()} is out!")
                    failure = True
                    break

            if not failure:
                print(f"\r[+] DETONATION CONFIRMED: {nation.upper()}")
                time.sleep(1.1)
            else:
                continue

        else:
            while not session.eject(nation):
                print(f"\r[!] Bomb bay doors stuck closed!")
                fails += 1
                if fails > 3:
                    print(f"\r[!] Three strikes and {nation.upper()} is out!")
                    failure = True
                    break

            if not failure:
                print(f"\r[+] DETONATION CONFIRMED: {nation.upper()}")
                time.sleep(1.1)

    print(f"[+] AIRSTRIKE COMPLETE. RETURNING TO BASE.")
else:
    print("Login failed. Check your credentials, ya dingus.")
