import discord
from discord.ext import commands

import json
import os

DESCRIPTION = "A music discord bot"

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    prefix = config["PREFIX"]


class Laleousa(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(
            command_prefix=prefix,
            description=DESCRIPTION,
            intents=intents,
        )
        self._load_extensions()

    def _load_extensions(self) -> None:
        cogs_dir = os.listdir("cogs")
        for filename in cogs_dir:
            if filename.endswith(".py"):
                cog = filename[:-3]
                self.load_extension(f"cogs.{cog}")
