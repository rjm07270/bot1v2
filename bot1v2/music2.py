import discord
from discord.ext import commands
import youtube_dl
import asyncio

class music2(commands.Cog):
    def __init__(self, client):
        print('loaded')
        
    """description of class"""
    @commands.command(name='join', help='This command makes the bot join the voice channel')
    async def join(self,ctx):
        if ctx.author.voice is None:
            await ctx.send("Get into a channel")
        else:
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)

    @commands.command(name='queue', help='This command adds a song to the queue')
    async def queue_(ctx, url):
        global queue

        queue.append(url)
        await ctx.send(f'`{url}` added to queue!')

    @commands.command(name='remove', help='This command removes an item from the list')
    async def remove(ctx, number):
        global queue

        try:
            del(queue[int(number)])
            await ctx.send(f'Your queue is now `{queue}!`')
    
        except:
            await ctx.send('Your queue is either **empty** or the index is **out of range**')
        
    @commands.command(name='play', help='This command plays songs')
    async def play(self,ctx):
        global queue
        print("test")
        server = ctx.message.guild
        voice_channel = ctx.voice_client

        YDL_OPTIONS = {'format': "bestaudio"}
        YTDLSource=None
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            YTDLSource =info['formats'][0]['url']

        

        async with ctx.typing():
            player = await YTDLSource.from_url(queue[0], loop=client.loop)
            voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('**Now playing:** {}'.format(player.title))
        del(queue[0])

    @commands.command(name='pause', help='This command pauses the song')
    async def pause(ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client

        voice_channel.pause()

    @commands.command(name='resume', help='This command resumes the song!')
    async def resume(ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client

        voice_channel.resume()

    @commands.command(name='view', help='This command shows the queue')
    async def view(ctx):
        await ctx.send(f'Your queue is now `{queue}!`')

    @commands.command(name='leave', help='This command stops makes the bot leave the voice channel')
    async def leave(ctx):
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()

    @commands.command(name='stop', help='This command stops the song!')
    async def stop(ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client

        voice_channel.stop()

def setup(client):
    client.add_cog(music2(client))