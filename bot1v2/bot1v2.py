import discord
from discord.ext import commands
import music
import joke

cogs = [music,joke]

client = commands.Bot(command_prefix='1!', intents = discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)


client.run("ODk5NTE1MTA0ODIxOTAzMzYw.YWz4uQ.JxIKZE5qghWrFF-ogdtjOpmWIh8")
