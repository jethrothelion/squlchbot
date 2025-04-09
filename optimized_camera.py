import cv2
import time
import asyncio
from pathlib import Path
import discord
from discord.ext import tasks, commands

camera_path = "motion_log.txt"
current_path = Path.cwd()
bot = discord.ext.commands.Bot(command_prefix = "!", intents=discord.Intents().all())

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

    await bot.change_presence(activity=discord.Game(name="raconfeburgnite"))
    global opusexe
    discord.opus.load_opus(opusexe)
    print('hewo')

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
