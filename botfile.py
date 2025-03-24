import asyncio
import datetime
import os
import pathlib
import random
from datetime import datetime
from pathlib import Path
import discord
from discord.ext import tasks, commands
import cv2
from ip import start_server

# Check and reset the camera before importing standalonecamera
print("Releasing any previous camera instance...")
camera = cv2.VideoCapture(0)
camera.release()
camera = None
print("Camera released successfully!")

# Now import standalonecamera safely
import standalonecamera


bot = discord.ext.commands.Bot(command_prefix = "!", intents=discord.Intents().all())



ytdlpexe = "C:\\Users\\Corey\\Downloads\\yt-dlp.exe"
opusexe = r"C:\Users\Corey\Downloads\libopus-0.x64.dll"
ffmpegexe = r"C:\ffmpeg\bin\ffmpeg.exe"
sections_to_run = list()
CHANNEL_ID = 834800817042096131
current_path = Path.cwd()
secCamPath = r'C:\ContaCam\USB HDCam '
camera_path = "motion_log.txt"



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

#startup
text = """
What services would you like active?
1. camera motion detection
2. ip communication
3. announcements
"""
input = input(text)
if "1" in input:
    sections_to_run.append("1")
if "2" in input:
    sections_to_run.append("2")
if "3" in input:
    sections_to_run.append("3")



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

    await bot.change_presence(activity=discord.Game(name="raconfeburgnite"))
    global opusexe
    discord.opus.load_opus(opusexe)
    print('hewo')



async def on_guild_join(message, self, guild, member: discord.Member):
    if member.__contains__("755069362418745385"):
        await member.ban(reason="reason")
        await message.channel.send(f'User {member} has been kick')



@bot.event
async def on_reaction_add(reaction, user, channel):
    print("reaction added" + reaction + user + channel)

@bot.event
async def on_message(message, user: discord.Member = None):
    username = str(message.author).split("#")[0]
    user_message = str(message.content).lower()
    channel = str(message.channel)
    print(f"{username}: {user_message} ({channel})")
    user = message.author

    stripmsg = channel + " " + username + " " + user_message

    await bot.process_commands(message)

    finalFilename = None
    if user_message.__contains__("todays forecast is"):
        med = "💊"
        await message.add_reaction(med)

    # reminder trxt system
    if user_message.__contains__("morning todays forecast"):
        Me2ssage = await message.channel.send('Timers?')
        thumb_up = '👍'
        thumb_down = '👎'

        await Me2ssage.add_reaction(thumb_up)
        await Me2ssage.add_reaction(thumb_down)

        global totalsummer
        global Cbray
        global Rbray
        global Gbray
        y = str(message.author)
        if y != ("Python Final Progect"):
            check = lambda reaction, user: bot.user != user
            await bot.wait_for("reaction_add")
            x = await message.channel.send(totalsummer + "days till summer" + "\n" "more?")
            await x.add_reaction(thumb_up)
            if y != "Python Final Progect":
                await bot.wait_for("reaction_add")
                await message.channel.send(
                    Cbray + "till Coreys birthday" + "\n" + Rbray + "till ryleis birthday" + "\n" + Gbray + "till gs brithday" + "\n")

    finalFilename = None
    if username != bot.user.name:
        cmdpart = user_message[:7]

        if cmdpart.__contains__("play"):
            if message.author.voice == None:
                await message.channel.send("cant play anything your not in a vc dumbass")
            voice_channel = message.author.voice.channel
            voice_Client = await voice_channel.connect()
            curnt_audio = current_path / "media"
            curnt_audio_str = str(curnt_audio)

            search = message.content[4:]
            opts = (
                f"--no-playlist --force-ipv4 --default-search ytsearch "
                f"--extract-audio --audio-format mp3 "
                f"-x -o \"{curnt_audio_str}\output.%(ext)s\""
            )

            try:
                print("Downloading audio...")
                os.system(f'{ytdlpexe} "ytsearch:{search}" {opts}')
                print("Download may be complete")
            except Exception as e:
                print(f"Download error: {e}")

            mp3_file = f"{curnt_audio_str}\output.mp3"

            await message.channel.send("Playing " + user_message[4:])

            print(finalFilename)
            global ffmpegexe

            voice_Client.play(discord.FFmpegPCMAudio(executable=ffmpegexe, source=(mp3_file)))

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

async def sendCameradata(dataPath):
    camera_chanel = bot.get_channel(1186067959479812126)

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

                camera_chanel = bot.get_channel(1186067959479812126)

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
    print("3")
    # Run bot start and log reading concurrently
    parts = []
    if "1" in sections_to_run:
        parts.append(compare_logfile(camera_path))
        parts.append(standalonecamera.full())
    if "2" in sections_to_run:
        parts.append(start_server())
    if "3" in sections_to_run:
        parts.append()

    await asyncio.gather(bot.start(TOKEN), *parts)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
