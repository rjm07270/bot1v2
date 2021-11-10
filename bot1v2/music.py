import discord
from discord.ext import commands
import youtube_dl
import asyncio


class NoTracksFound(commands.CommandError):
    pass

class music(commands.Cog):
    def __init__(self, client):
        self.client =client
        self.queues={}
        self.Tqueues={}
        self.players={}
        self.is_playing=False

        
    def check_queue(self,ctx,id):

        if self.queues[id] != []:
            source =self.queues[id].pop(0)
            voice =ctx.guild.voice_client
            player=voice.play(source, after=lambda x=None: self.check_queue(ctx,id))


    @commands.command()
    async def join(self,ctx):
        if ctx.author.voice is None:
            await ctx.send("Get into a channel")
        else:
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)


    @commands.command()
    async def disconnect(self,ctx):
        if ctx.author.voice is None:
            await ctx.voice_client.disconnect()
    
    @commands.command()
    async def play(self,ctx,url):
        if ctx.author.voice is None:
            await ctx.send("Get into a channel")
        else:
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()


        ctx.voice_client.stop()
        url=url.strip("<>")
        FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}
        vc = ctx.voice_client
        
        info=None
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            ur12 =info['formats'][0]['url']
            
            source = await discord.FFmpegOpusAudio.from_probe(ur12, **FFMPEG_OPTIONS)
            
        guild_id = ctx.message.guild.id


        vc.play(source, after=lambda x=None: self.check_queue(ctx,guild_id))
        
        

    @commands.command()
    async def pause(self,ctx):
        await ctx.voice_client.pause()
        await ctx.send("pause")

    @commands.command()
    async def stop(self,ctx):
        await ctx.voice_client.stop()
        await ctx.send("stopped")

    @commands.command()
    async def queue(self,ctx,url):
        server= ctx.guild.voice_client
        FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}
        info=None
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            ur12 =info['formats'][0]['url']
            
            source = await discord.FFmpegOpusAudio.from_probe(ur12, **FFMPEG_OPTIONS)
            
        guild_id = ctx.message.guild.id

        if guild_id in self.queues:
            self.queues[guild_id].append(source)
            self.Tqueues[guild_id].append(info['duration'])
        else:
            self.queues[guild_id]= [source]
            self.Tqueues[guild_id]= [info['duration']]
        
        await ctx.send("added to queue")
def setup(client):
    client.add_cog(music(client))
