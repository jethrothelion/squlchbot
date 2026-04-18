import asyncio
import time
import datetime
import random
from datetime import datetime
from pathlib import Path
import discord
from discord.ext import tasks, commands




bot = commands.Bot(command_prefix = "!", intents=discord.Intents.all())


cameraid = 1368845660249522196
ytdlpexe = "C:\\Users\\Corey\\Downloads\\yt-dlp.exe"
opusexe = r"D:\opus\libopus-0.x64.dll"
ffmpegexe = r"C:\ffmpeg\bin\ffmpeg.exe"
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
            actual_message = user_message[4:].strip()  # strip "talk" from front
            if cmdpart.__contains__("talk"):
                ListeningFlag = True


                AIMessenger.add_message(user,actual_message)
                reply = await asyncio.get_event_loop().run_in_executor(None, AIMessenger.generate)
                await message.channel.send(reply)

            elif cmdpart.__contains__("stop talking"):
                ListeningFlag = False
                AIMessenger.clear_context()
                await message.channel.send("Context cleared.")
            elif ListeningFlag == True:
                AIMessenger.add_message(user, actual_message)
                reply = await asyncio.get_event_loop().run_in_executor(None, AIMessenger.generate)
                await message.channel.send(reply)
        if cmdpart.__contains__("play"):
            print(stripmsg)

            if message.guild is None:
                await message.channel.send("You can't use voice commands in DMs.")
                return

            if message.author.voice == None:
                await message.channel.send("cant play anything your not in a vc dumbass")
                return

            voice_channel = message.author.voice.channel
            # REPLACE with:
            voice_Client = discord.utils.get(bot.voice_clients, guild=message.guild)
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
                    await message.channel.send(f"failed to connect: {e}")
                    return

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
                process = await asyncio.create_subprocess_shell(f'{ytdlpexe} "ytsearch:{search}" {opts}')
                await process.communicate()
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
    print("3")
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