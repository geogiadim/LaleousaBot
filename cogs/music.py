import discord
from discord.ext import commands
import youtube_dl

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}
YDL_OPTIONS = {'format': "bestaudio"}


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Bot is online")

    @commands.command(name='leave')
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name='join')
    async def join(self, ctx):
        if ctx.author.voice is None:
            print('asdsada')
            await ctx.send("You are not in a voice channel!")
        else:
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)

    @commands.command(name='play')
    async def play(self, ctx, url):
        ctx.voice_client.stop()
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command(play='pause')
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Paused")

    @commands.command(play='resume')
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Resumed")



def setup(bot):
    bot.add_cog(Music(bot))
