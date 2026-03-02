# utils/cog/loader.py
import os
import importlib
import traceback
import sys
from colorama import Fore, Style, init

sys.dont_write_bytecode = True
init(autoreset=True)

async def load_commands(bot):
    loaded = 0
    failed = 0

    for root, _, files in os.walk("commands"):
        for file in files:
            if not file.endswith(".py") or file.startswith("_"):
                continue

            file_path = os.path.join(root, file)
            module_path = file_path.replace(os.sep, ".")[:-3]

            try:
                module = importlib.import_module(module_path)

                if getattr(module, "COG", False) is True:
                    await bot.load_extension(module_path)
                    print(f"{Fore.CYAN}[INFO] {Fore.LIGHTBLACK_EX}- Loaded command: {Fore.GREEN}{module_path}")
                    loaded += 1
                else:
                    print(f"{Fore.CYAN}[INFO] {Fore.LIGHTBLACK_EX}- Skipped (COG not True): {Fore.LIGHTBLUE_EX}{module_path}")

            except Exception:
                print(f"{Fore.RED}[ERROR] Failed to load command: {Fore.LIGHTBLUE_EX}{module_path}")
                print(Fore.RED + traceback.format_exc())
                failed += 1

    print(f"{Fore.CYAN}[INFO] {Fore.LIGHTBLACK_EX}- Commands Loaded: {Fore.GREEN}{loaded} | Failed: {Fore.RED}{failed}")


async def load_events(bot):
    loaded = 0
    failed = 0

    for root, _, files in os.walk("events"):
        for file in files:
            if not file.endswith(".py") or file.startswith("_"):
                continue

            file_path = os.path.join(root, file)
            module_path = file_path.replace(os.sep, ".")[:-3]

            try:
                module = importlib.import_module(module_path)

                if getattr(module, "COG", False) is True:
                    await bot.load_extension(module_path)
                    print(f"{Fore.CYAN}[INFO] {Fore.LIGHTBLACK_EX}- Loaded event: {Fore.GREEN}{module_path}")
                    loaded += 1
                else:
                    print(f"{Fore.CYAN}[INFO] {Fore.LIGHTBLACK_EX}- Skipped (COG not True): {Fore.LIGHTBLUE_EX}{module_path}")

            except Exception:
                print(f"{Fore.RED}[ERROR] Failed to load event: {Fore.LIGHTBLUE_EX}{module_path}")
                print(Fore.RED + traceback.format_exc())
                failed += 1

    print(f"{Fore.CYAN}[INFO] {Fore.LIGHTBLACK_EX}- Events Loaded: {Fore.GREEN}{loaded} | Failed: {Fore.RED}{failed}")