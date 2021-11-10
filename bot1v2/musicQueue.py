import discord
from discord.ext import commands, tasks
import youtube_dl
import asyncio

class musicQueue(object):
    """description of class"""
    def __init__(self, client,ctx):
        self.queues={}
        self.Tqueues={}
        self.ctx=ctx

    async def start():
        server= self.ctx.guild.voice_client
        FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}
        info=None
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            ur12 =info['formats'][0]['url']
            
            source = await discord.FFmpegOpusAudio.from_probe(ur12, **FFMPEG_OPTIONS)
            
        guild_id = self.ctx.message.guild.id

        if guild_id in self.queues:
            self.queues[guild_id].append(source)
            self.Tqueues[guild_id].append(info['duration'])
        else:
            self.queues[guild_id]= [source]
            self.Tqueues[guild_id]= [info['duration']]
        
        await self.ctx.send("added to queue")
@tasks.loop(seconds=Tqueues[])