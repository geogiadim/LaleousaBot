import discord
from discord.ext import commands
import youtube_dl
from requests import get

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}
YDL_OPTIONS = {'format': "bestaudio"}


def ytb_search(arg):
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            get(arg)
        except:
            info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        else:
            info = ydl.extract_info(arg, download=False)

    return {
        "source": info["formats"][0]["url"],
        "title": info["title"],
        "duration": info["duration"],
    }


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Bot is online")

    @commands.command(name='join', help="Connect to a voice channel")
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Please connect to a voice channel!")
        else:
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
                print("Joined: ", voice_channel)
            else:
                await ctx.voice_client.move_to(voice_channel)
                print("Joined: ", voice_channel)

    @commands.command(name='play', help="Play s youtube_url or youtube query")
    async def play(self, ctx, *args):
        if ctx.voice_client is not None:
            ctx.voice_client.stop()
            vc = ctx.voice_client

            query = " ".join(args)
            song = ytb_search(query)

            await ctx.send(f""":headphones: **{song["title"]}** has been added to the queue by {ctx.author.mention}""")

            source = await discord.FFmpegOpusAudio.from_probe(song["source"], **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command(name='leave', help="Disconnect from the voice channel")
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            print("Disconnected")

    @commands.command(play='pause', help="Pause playing song")
    async def pause(self, ctx):
        if ctx.voice_client is not None:
            ctx.voice_client.pause()
            await ctx.send(f""":headphones: Paused""")

    @commands.command(play='resume', help="Resume playing song")
    async def resume(self, ctx):
        if ctx.voice_client is not None:
            ctx.voice_client.resume()
            await ctx.send(f""":headphones: Resumed""")


def setup(bot):
    bot.add_cog(Music(bot))
