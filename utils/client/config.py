# utils/client/config.py
import os
import time
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

ENV_PATH = Path(".env")

def create_env():
    print(f"{Fore.CYAN}> Dynasty Setup")
    print(f"{Fore.LIGHTBLACK_EX}- .env is missing, proceeding to setup..")
    time.sleep(2)
    os.system("cls" if os.name == "nt" else "clear")
    
    print(f"{Fore.CYAN}> Dynasty Setup")
    prefix = input(f"{Fore.LIGHTBLUE_EX}> Enter Your Bot Prefix: {Style.RESET_ALL}").strip() or "?"
    print(f"{Fore.GREEN}> Saved Bot Prefix: {prefix}\n")
    
    token = input(f"{Fore.LIGHTBLUE_EX}> Enter Your Bot Token: {Style.RESET_ALL}").strip()
    print(f"{Fore.GREEN}> Saved Bot Token: {'*' * 6 + token[-4:]}")
    
    with ENV_PATH.open("w") as f:
        f.write(f'BOT_PREFIX="{prefix}"\n')
        f.write(f'BOT_TOKEN="{token}"\n')
    
    time.sleep(1)
    os.system("cls" if os.name == "nt" else "clear")

if not ENV_PATH.exists():
    create_env()

BOT_TOKEN = None
BOT_PREFIX = None

with ENV_PATH.open("r") as f:
    for line in f:
        if line.startswith("BOT_TOKEN"):
            BOT_TOKEN = line.strip().split("=", 1)[1].strip().strip('"')
        elif line.startswith("BOT_PREFIX"):
            BOT_PREFIX = line.strip().split("=", 1)[1].strip().strip('"')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env")
if not BOT_PREFIX:
    BOT_PREFIX = "?"