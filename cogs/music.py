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
        self.current_song = None
        self.songs_queue = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Bot is online")

    @commands.command(name='join', help="Connects to a voice channel")
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

    def play_next(self, vc):
        if len(self.songs_queue) > 0:
            self.is_playing = True
            song_url = self.songs_queue[0][0]["source"]
            self.current_song = self.songs_queue.pop(0)
            vc.play(
                discord.FFmpegPCMAudio(song_url, **FFMPEG_OPTIONS),
                after=lambda e: self.play_next(vc),
            )
        else:
            self.is_playing = False
            self.current_song = None

    @commands.command(name='play', help="Plays youtube_url or youtube query")
    async def play(self, ctx, *args):
        if ctx.voice_client is not None:
            vc = ctx.voice_client

            query = " ".join(args)
            song = ytb_search(query)

            self.songs_queue.append([song, ctx.author.mention])
            await ctx.send(f""":headphones: **{song["title"]}** has been added to the queue by {ctx.author.mention}""")

            if not self.is_playing:
                self.is_playing = True
                self.current_song = self.songs_queue.pop(0)
                vc.play(
                    discord.FFmpegPCMAudio(song["source"], **FFMPEG_OPTIONS),
                    after=lambda e: self.play_next(vc),
                )

    @commands.command(name='q', help="Prints song playlist in queue")
    async def print_queue(self, ctx):
        print(self.songs_queue)
        result = ""
        for i, song in enumerate(self.songs_queue):
            result += f"""{i+1}. **{song[0]['title']}** -- added by {song[int(1)]}\n"""

        if result != "":
            await ctx.send(result)
        else:
            await ctx.send("Empty queue")

    @commands.command(name="cq", help="Clears songs queue")
    async def clear_queue(self, ctx):
        self.songs_queue = []
        await ctx.send("""***Queue cleared!!!***""")

    @commands.command(name="skip", help="Skips the current song being played",)
    async def skip(self, ctx):
        if ctx.voice_client is not None:
            ctx.voice_client.stop()
            self.is_playing = False
            await ctx.send(f"""**Skipped**-- {self.current_song[0]['title']}""")

            if not self.is_playing:
                if len(self.songs_queue) > 0:
                    self.is_playing = True
                    self.current_song = self.songs_queue.pop(0)
                    ctx.voice_client.play(
                        discord.FFmpegPCMAudio(self.songs_queue[0][0]["source"], **FFMPEG_OPTIONS),
                        after=lambda e: self.play_next(ctx.voice_client),
                    )

    # @commands.command(name="rm", help="Removes a song from queue at given index")
    # async def remove(self, ctx, *args):
    #     if ctx.voice_client is not None:
    #         query = "".join(*args)
    #         index = int(query)
    #
    #         if index >= len(self.songs_queue) or index < 1:
    #             await ctx.send("Invalid Index")
    #         else:
    #             self.songs_queue.pop(index)
    #             await ctx.send(f""":x: {self.songs_queue[index-1][0]['title']} -- removed by {ctx.author.mention}""")

    @commands.command(name='leave', help="Disconnects from the voice channel")
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            self.is_playing = False
            self.current_song = None
            self.songs_queue = []
            await ctx.voice_client.disconnect()
            print("Disconnected")

    @commands.command(play='pause', help="Pause playing song")
    async def pause(self, ctx):
        if ctx.voice_client is not None:
            if self.is_playing:
                ctx.voice_client.pause()
                await ctx.send(f""":pause_button: **Paused** -- {self.current_song[0]['title']}""")

    @commands.command(play='resume', help="Resume playing song")
    async def resume(self, ctx):
        if ctx.voice_client is not None:
            if self.is_playing:
                ctx.voice_client.resume()
                await ctx.send(f""":arrow_forward: **Resumed** -- {self.current_song[0]['title']}""")


def setup(bot):
    bot.add_cog(Music(bot))
