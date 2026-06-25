import asyncio
import time
import datetime
import random
from datetime import datetime
from pathlib import Path
import discord
from discord.ext import tasks, commands



bot = commands.Bot(command_prefix = "!", intents=discord.Intents.all())
tree = bot.tree

ytdlpexe = "C:\\Users\\Corey\\Downloads\\yt-dlp.exe"
if not Path(ytdlpexe).exists():
    ytdlpexe = "yt-dlp"

opusexe = r"D:\opus\libopus-0.x64.dll"
if not Path(opusexe).exists():
    opusexe = "libopus"

ffmpegexe = r"C:\ffmpeg\bin\ffmpeg.exe"
if not Path(ffmpegexe).exists():
    ffmpegexe = "ffmpeg"


cameraid = 1368845660249522196
sections_to_run = list()
current_path = Path.cwd()
secCamPath = r'C:\ContaCam\USB HDCam '
camera_path = "motion_log.txt"

global ListeningFlag
ListeningFlag = False


#env variable file keyying
env_data = {}
env_file = current_path / "env.txt"
with open(env_file, "r") as file:
    for line in file:
        if not line.strip():
            continue
        # Split the line into key and value, stripping any leading or trailing whitespaces
        key, value = map(str.strip, line.split("="))
        env_data[key.lower()] = value

#startup gather done now so dont have to wait to process
text = """
What services would you like active?
1. camera motion detection
2. ip communication
3. local ai bot responses
4. basic bot functions
"""
input = input(text)
if "1" in input:
    sections_to_run.append("1")
    import cv2
    import standalonecamera
if "2" in input:
    sections_to_run.append("2")
    from ip import start_server
if "3" in input:
    sections_to_run.append("3")
    import AIMessenger

if "4" in input:
    sections_to_run.append("4")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    await bot.change_presence(activity=discord.Game(name="raconfeburgnite"))

    synced = await bot.tree.sync()
    print(f"synced {len(synced)} slash commands")

    global opusexe
    try:
        discord.opus.load_opus(opusexe)
    except Exception as e:

        print(f'exception in loading opus: {e}')


@bot.event
async def on_member_join(member: discord.Member):
    if "755069362418745385" in str(member.id):
        await member.ban(reason="reason")
        if member.guild.system_channel:
            await member.guild.system_channel.send(f'User {member} has been kick')


@bot.event
async def on_reaction_add(reaction, user):
    print(f"reaction added {reaction} {user} {reaction.message.channel}")


@bot.event
async def on_message(message, user: discord.Member = None):
    global ListeningFlag
    username = str(message.author).split("#")[0]
    user_message = str(message.content).lower()
    channel = str(message.channel)
    print(f"{username}: {user_message} ({channel})")
    user = message.author

    stripmsg = channel + " " + username + " " + user_message

    await bot.process_commands(message)

    finalFilename = None
    if username != bot.user.name:
        cmdpart = user_message[:15]

        if "3" in sections_to_run:
            if ListeningFlag == True:
                print("talking")
                AIMessenger.add_message(user_message, username)
                output = AIMessenger.run_model()
                await message.channel.send(output)
                print("past talk")
            if cmdpart.__contains__("start talk"):
                ListeningFlag = True
                print("starting talking")
            if cmdpart.__contains__("stop talk"):
                ListeningFlag = False
                print("stopping talking")

        if cmdpart.__contains__("purge"):
            print(message.channel.last_message())
        if cmdpart == "random":
            await message.channel.send(f"this is your random number: {random.randrange(1000000)}")
            return
        if "fortnite" in user_message:
            await message.channel.send(f"fortnite balls game 6000 dick dancer dababy")
            return
        if "fog" in user_message:
            await message.channel.send(f"desharen")
            return
        channelstr = str(channel)

        if "Direct Message" in channelstr:
            await message.channel.send("skibidie toiliet centeral")
            return
        if f"help" in user_message:
            await message.channel.send("skunk twerk")
            return
        if "bbl" in user_message:
            await message.channel.send("drizzzzayy")


@bot.event
async def on_message_edit(before, after):
    print(
        f"{before.author}edit a message. \n"
        f"before: {before.content}\n"
        f"after: {after.content}"
    )


@bot.tree.command(name="play", description="Plays youtube video")
async def play(interaction: discord.Interaction, *, search: str):
    await interaction.response.defer()

    if interaction.guild is None:
        await interaction.followup.send("You can't use voice commands in DMs.")
        return
    if interaction.user.voice is None:
        await interaction.followup.send("cant play anything your not in a vc dumbass")
        return

    voice_channel = interaction.user.voice.channel
    voice_Client = discord.utils.get(bot.voice_clients, guild=interaction.guild)


    #VOICE CONNECTION LOGIC
    if voice_Client and voice_Client.is_connected():
        print("moving to " + str(voice_Client))
        await voice_Client.move_to(voice_channel)
    else:
        print("connecting to " + str(voice_channel))
        try:
            voice_Client = await voice_channel.connect()
            print("connected successfully to " + str(voice_channel))
        except Exception as e:
            print(f"connect error: {e}")
            await interaction.followup.send(f"failed to connect: {e}")
            return

    if voice_Client.is_playing():
        voice_Client.stop()

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    #GET VIDEO URL
    if search.startswith("https"):
        page_url = search
        proc = await asyncio.create_subprocess_shell(
            f'{ytdlpexe} -f bestaudio --print "%(title)s" --print "%(url)s" "ytsearch:{page_url}"',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout_bytes, stderr_bytes = await proc.communicate()
        if not stdout_bytes:
            await interaction.followup.send("couldnt get audio from that url")
            return
        lines = stdout_bytes.decode().strip().split('\n')
        title = lines[0]
        url = lines[1]

        source = discord.FFmpegPCMAudio(executable=ffmpegexe, source=url, **FFMPEG_OPTIONS)
        voice_Client.play(source)

    else:
        print(f"searching for video {search}")
        proc = await asyncio.create_subprocess_shell(
            f'{ytdlpexe} -f bestaudio --print "%(title)s" --print "%(webpage_url)s" --print "%(url)s" "ytsearch:{search}"',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout_bytes, stderr_bytes = await proc.communicate()
        if not stdout_bytes:
            await interaction.followup.send("couldnt find anything for: " + search)
            return
        lines = stdout_bytes.decode().strip().split('\n')
        title = lines[0]
        page_url = lines[1]
        url = lines[2]
        print(f"found url for {search}")

        source = discord.FFmpegPCMAudio(source=url)
        voice_Client.play(source)

    await interaction.followup.send(f"Now playing **{title}**\n{page_url}")


async def sendCameradata(dataPath):
    global cameraid
    camera_chanel = bot.get_channel(cameraid)

    await camera_chanel.send(file=discord.File(dataPath))

async def compare_logfile(file_path):
    print("hh")
    while True:
        #jus compares to files variable names dum cuz idk what else to name them
        try:
            with open(file_path, "r") as f:
                c = f.read()
            await asyncio.sleep(0.2)  # Change the duration as needed (e.g., 5 seconds)
            with open(file_path, "r") as f:
                d = f.read()

            if d != c:
                global cameraid
                camera_chanel = bot.get_channel(cameraid)

                logs = [entry.strip() for entry in d.split(":")]
                print(f"Logs after split: {logs}")
                if logs[0] == "detected":
                    print("logdetect")
                    clock = str(datetime.now())
                    await camera_chanel.send("camaera detected at " + clock)
                    print(logs[2])
                    picpath = logs[2]
                    await sendCameradata(picpath)

                if logs[0]== "recording":
                    vidpath = logs[2]
                    print(vidpath)
                    try: await sendCameradata(vidpath)
                    except Exception as e:
                        errorStr = str(e)
                        print(errorStr)
                        await camera_chanel.send("error file proabbly to big"+ errorStr)
        except FileNotFoundError:
            print("Log file not found, waiting for file to be created...")
        except Exception as e:
            print(f"Unexpected error in compare_logfile: {e}")



TOKEN = env_data.get("token")
async def main():
    # Run bot start and log reading concurrently
    parts = []
    if "1" in sections_to_run:
        parts.append(compare_logfile(camera_path))
        # Check and reset the camera before importing standalonecamera
        print("Releasing any previous camera instance...")
        camera = cv2.VideoCapture(0)
        camera.release()
        camera = None
        time.sleep(1)
        print("Camera released successfully!")

        # Now import standalonecamera safely
        import standalonecamera
        parts.append(standalonecamera.full())

    if "2" in sections_to_run:
        parts.append(start_server())
    if "3" in sections_to_run:
        pass
    if "4" in sections_to_run:
        pass
    await asyncio.gather(bot.start(TOKEN), *parts)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Shutting down")
        standalonecamera.stop_camera()
    finally:
        loop.run_until_complete(bot.close())
        loop.close()