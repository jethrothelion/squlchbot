import cv2
import time
import asyncio
from pathlib import Path
import discord
from discord.ext import tasks, commands
from datetime import datetime
import signal
import platform
import os

cameraid = 1368845660249522196
camera_path = "motion_log.txt"
current_path = Path.cwd()
bot = discord.ext.commands.Bot(command_prefix = "!", intents=discord.Intents().all())

# Signal handlers to safely release camera
def handle_sigtstp(signum, frame):
    global camera
    print("Caught SIGTSTP, releasing camera…")
    if camera is not None:
        camera.release()
        camera = None
        print("Camera released.")
    signal.signal(signal.SIGTSTP, signal.SIG_DFL)
    os.kill(os.getpid(), signal.SIGTSTP)

def handle_sigcont(signum, frame):
    global camera
    print("Resuming—reopening camera…")
    camera = cv2.VideoCapture(0)

def clean_up(signum=None, frame=None):
    global camera
    print("Cleaning up before exit…")
    if camera is not None:
        camera.release()
        camera = None
        print("Camera released.")
    if signum in (signal.SIGINT, signal.SIGTERM):
        raise SystemExit

# Safe cross-platform signal setup
signal.signal(signal.SIGINT, clean_up)
signal.signal(signal.SIGTERM, clean_up)

if platform.system() != "Windows":
    signal.signal(signal.SIGTSTP, handle_sigtstp)
    signal.signal(signal.SIGCONT, handle_sigcont)

# Check and reset the camera before importing standalonecamera
print("Releasing any previous camera instance...")
camera = cv2.VideoCapture(0)
camera.release()
camera = None
time.sleep(1)
print("Camera released successfully!")

# Now import standalonecamera safely
import standalonecamera

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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

    await bot.change_presence(activity=discord.Game(name="detecting motion"))
    print('hewo')

async def sendCameradata(dataPath):
    global cameraid
    camera_chanel = bot.get_channel(cameraid)

    await camera_chanel.send(file=discord.File(dataPath))

async def compare_logfile(file_path):
    global cameraid
    while True:
        #jus compares to files variable names dum cuz idk what else to name them
        try:
            with open(file_path, "r") as f:
                c = f.read()
            await asyncio.sleep(0.2)  # Change the duration as needed (e.g., 5 seconds)
            with open(file_path, "r") as f:
                d = f.read()

            if d != c:
                camera_chanel = bot.get_channel(cameraid)

                logs = [entry.strip() for entry in d.split(":")]
                if logs[0] == "detected":
                    clock = str(datetime.now())
                    await camera_chanel.send("camaera detected at " + clock)
                    picpath = logs[2]
                    await sendCameradata(picpath)

                if logs[0]== "recording":
                    vidpath = logs[2]
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
if not TOKEN:
    raise ValueError("Bot token not found in env.txt")

async def main():

    await asyncio.gather(bot.start(TOKEN), standalonecamera.full(),compare_logfile(camera_path))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        loop.run_until_complete(bot.close())
        loop.close()
