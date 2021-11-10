import discord
from discord.ext import commands
import youtube_dl
from requests import get
from cogs.utils.roles import voice_channel_moderator_roles

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


# @commands.command(name='join', help="Connects to a voice channel")
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("Please connect to a voice channel!")
    else:
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            print("Joined: ", voice_channel)
        else:
            if voice_channel != ctx.voice_client.channel:
                await ctx.voice_client.move_to(voice_channel)
                print("Joined: ", voice_channel)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.current_song = None
        self.songs_queue = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Bot is online")

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

    @commands.command(name='play', help="Adds in queue or plays the song given by YouTube url or query")
    async def play(self, ctx, *args):
        await join(ctx)
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

    @commands.command(name='q', help="Prints music queue")
    @commands.has_any_role(*voice_channel_moderator_roles)
    async def print_queue(self, ctx):
        print(self.songs_queue)
        result = ""
        for i, song in enumerate(self.songs_queue):
            result += f"""{i+1}. **{song[0]['title']}** -- added by {song[int(1)]}\n"""

        if result != "":
            await ctx.send(result)
        else:
            await ctx.send("Empty queue")

    @commands.command(name="cq", help="Clears music queue")
    @commands.has_any_role(*voice_channel_moderator_roles)
    async def clear_queue(self, ctx):
        self.songs_queue = []
        await ctx.send("""***Queue cleared!!!***""")

    @commands.command(name="skip", help="Skips the current music track")
    @commands.has_any_role(*voice_channel_moderator_roles)
    async def skip(self, ctx):
        if ctx.voice_client is not None:
            if self.is_playing:
                ctx.voice_client.stop()
                self.is_playing = False
                await ctx.send(f"""**Skipped** -- {self.current_song[0]['title']}""")

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
    @commands.has_any_role(*voice_channel_moderator_roles)
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            self.is_playing = False
            self.current_song = None
            self.songs_queue = []
            await ctx.voice_client.disconnect()
            print("Disconnected")

    @commands.command(name='pause', help="Pause playing music")
    async def pause(self, ctx):
        if ctx.voice_client is not None:
            if self.is_playing:
                ctx.voice_client.pause()
                await ctx.send(f""":pause_button: **Paused** -- {self.current_song[0]['title']}""")

    @commands.command(name='resume', help="Resume playing music")
    async def resume(self, ctx):
        if ctx.voice_client is not None:
            if self.is_playing:
                ctx.voice_client.resume()
                await ctx.send(f""":arrow_forward: **Resumed** -- {self.current_song[0]['title']}""")

    @commands.command(name='mitsotakigamiesai', help="KATEVASE TO SE PARAKALW")
    async def mg(self, ctx):
        await self.play(ctx, "https://www.youtube.com/watch?v=k99YAA6cn2Q&ab_channel=FilmAckrakin")

    @commands.command(name='madclip', help="Money And Drugs Can't Live In Poverty")
    async def mad_clip(self, ctx):
        await self.play(ctx, "https://www.youtube.com/watch?v=8rKWHn2cPnc")

    @commands.command(name='compactitaly', help="Oi megalyteres italikes epitixies olwn twn epoxwn")
    async def compact_italy(self, ctx):
        await self.play(ctx, "https://www.youtube.com/watch?v=PzhVvG-1tpE&ab_channel=NatashaI")

    @commands.command(name='compactillusions', help="Eikones plasmenes apo oneira")
    async def compact_illusions(self, ctx):
        await self.play(ctx, "https://www.youtube.com/watch?v=yQwMV5aJWRQ")

    @commands.command(name='compactfairytales', help="H mousiki moiazei me paramithi")
    async def compact_fairytales(self, ctx):
        await self.play(ctx, "https://www.youtube.com/watch?v=EqujUeTGckY")

    @commands.command(name='compactstratos', help="Xoros ellinikos, antrikos, varus!!")
    async def compact_zeimpekika(self, ctx):
        await self.play(ctx, "https://www.youtube.com/watch?v=Ese1ahsa0OU")

    @commands.command(name='mitsotaki', help="KATEVASE TO DEN THA TO XANAPW")
    async def mitsotaki(self, ctx):
        await ctx.send(f"""**GAMIESAI RE MALAKA**""")

    @commands.command(name="vanskip", help="Skips the current music track")
    async def van_skip(self, ctx):
        await self.skip(ctx)


def setup(bot):
    bot.add_cog(Music(bot))
