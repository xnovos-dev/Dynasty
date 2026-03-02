# utils/cog/loader.py
import os
import importlib
from discord.ext import commands

async def load(bot: commands.Bot, base_path="."):
    """
    Recursively loads all command and event Cogs
    
    Example structure:
    main.py
    Commands/
        Utility/ping.py
    Events/
        Client/on_ready.py
    """
    loaded = []
    failed = []

    for root, dirs, files in os.walk(base_path):
        if any(part.startswith(".") for part in root.split(os.sep)) or "utils" in root:
            continue

        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                relative_path = os.path.relpath(os.path.join(root, file), ".")
                module_path = relative_path.replace(os.sep, ".")[:-3]

                try:
                    module = importlib.import_module(module_path)

                    for attr in dir(module):
                        obj = getattr(module, attr)
                        if isinstance(obj, type) and issubclass(obj, commands.Cog):
                            cog_instance = obj(bot)
                            await bot.add_cog(cog_instance)
                            loaded.append(module_path)
                            break
                except Exception as e:
                    failed.append((module_path, e))

    return loaded, failed