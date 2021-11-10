import discord
from discord.ext import commands
import requests
import json

badWords=['unemployed','lol says you','fudk','dipshit','bot','homo','dogwater','cracker','dog','lame','fucksake','bitchboy','old','senial','fuck', 'bitch','gay','ass','bastard','piss','liar','hoe','stupid','dumb','fag','whore','nerd','cunt','pussy','asshole','fucker','dumbass','idot','shithead','shit']
#329460286086053889
class joke(commands.Cog):
    """description of class"""
    def __init__(self, client):
        self.client =client
    @commands.command()
    async def insult(self,ctx):
        data= requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
        jsonData=data.json()
        insult =jsonData['C']
        await ctx.send(insult)

def setup(client):
    client.add_cog(joke(client))

