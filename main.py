import discord
from discord.ext import commands
import music

intents = discord.Intents.default()
intents.members = True

DESCRIPTION = "A music discord bot"

client = commands.Bot(command_prefix='?', description=DESCRIPTION, intents=intents)

cogs = [music]
for i in range(len(cogs)):
    cogs[i].setup(client)

client.run('__YOUR TOKEN HERE__')
