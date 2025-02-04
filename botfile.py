import datetime
from datetime import datetime
import discord
import random
from discord.ext import tasks, commands
import aiocron
from datetime import date
import requests
from bs4 import BeautifulSoup
import yt_dlp as youtube_dl
import UIonwakeup
from ip2geotools.databases.noncommercial import DbIpCity
import asyncio
import socket
import nacl
import pyautogui
import os

CHANNEL_ID = 834800817042096131



bot = discord.ext.commands.Bot(command_prefix = "!", intents=discord.Intents().all())

#env variable file keyying
env_data = {}
with open("C:/discord bot/discord-bot-dev-branch/env.txt", "r") as file:
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
    discord.opus.load_opus(r"C:\Users\Corey\Downloads\libopus-0.x64.dll")
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
    ytdlpexe = "C:\\Users\\Corey\\Downloads\\yt-dlp.exe"
    username = str(message.author).split("#")[0]
    user_message = str(message.content).lower()
    channel = str(message.channel)
    print(f"{username}: {user_message} ({channel})")
    user = message.author

    stripmsg = channel + " " + username + " " + user_message

    await bot.process_commands(message)

    finalFilename = None
    if username != bot.user.name:
        cmdpart = user_message[:7]

        if cmdpart.__contains__("play"):
            print(message.author.voice)
            if message.author.voice == None:
                await message.channel.send("cant play anything your not in a vc dumbass")
            voice_channel = message.author.voice.channel
            voice_Client = await voice_channel.connect()

            search = message.content[4:]
            opts = "--no-playlist --force-ipv4 --paths C:\yt-dlp --extract-audio --audio-format mp3 -o C:\yt-dlp\curnt-audio.mp3"
            try:
                os.system(f'{ytdlpexe} "ytsearch:{search}" {opts}')
            except Exception as e:
                print("e")

            await message.channel.send("Playing " + user_message[4:])

            print(finalFilename)

            source = discord.FFmpegPCMAudio(executable=r"C:\ffmpeg\bin\ffmpeg.exe", source=r"C:\discord bot\Fartsoundeffect.mp3")
            voice_Client.play(discord.FFmpegPCMAudio(executable=r"C:\ffmpeg\bin\ffmpeg.exe", source=("C:\yt-dlp\curnt-audio.webm")))

            return
        if cmdpart.__contains__("purge"):
            print(message.channel.last_message())
        if cmdpart == "random":
            await message.channel.send(f"this is your random number: {random.randrange(1000000)}")
            return
        if user_message.__contains__("fortnite"):
            await message.channel.send(f"fortnite balls game 6000 dick dancer dababy")
            return
        if user_message.__contains__("fog"):
            await message.channel.send(f"desharen")
            return
        channelstr = str(channel)
        if channelstr.__contains__("Direct Message"):
            await message.channel.send("skibidie toiliet centeral")
            return
        if user_message.__contains__(f"help"):
            await message.channel.send("skunk twerk")
            return
        if "bbl" in user_message:
            await message.channel.send("drizzzzayy")
       #for ip comunication
        await send_message(client, stripmsg)



@bot.event
async def on_message_edit(before, after):
    print(
        f"{before.author}edit a message. \n"
        f"before: {before.content}\n"
        f"after: {after.content}"
    )


secCamPath = r'C:\ContaCam\USB HDCam '

async def sendCameradata(dataPath):
    camera_chanel = bot.get_channel(1186067959479812126)

    await camera_chanel.send(file=discord.File(dataPath))

camera_path = "detection.txt"
async def compare_logfile(file_path):
    print("hh")
    while True:
        #jus compares to files variable names dum cuz idk what else to name them
        f = open(file_path, "r")
        c = f.read()
        await asyncio.sleep(0.2)  # Change the duration as needed (e.g., 5 seconds)
        x = open(file_path, "r")
        d = x.read()

        if d != c:

            camera_chanel = bot.get_channel(1186067959479812126)
            logs = d.split(":")

            if logs[0] == "detected":
                clock = str(datetime.now())
                await camera_chanel.send("camaera detected at" + clock)
                picpath = secCamPath + logs[1]
                await sendCameradata(picpath)

            if logs[0]== "recordin":
                vidpath = secCamPath + logs[1]
                try: await sendCameradata(vidpath)
                except Exception as e:
                    errorStr = str(e)
                    print(errorStr)
                    await camera_chanel.send("error file proabbly to big"+ errorStr)



TOKEN = env_data.get("token")
async def main():
    # Run bot start and log reading concurrently
    await asyncio.gather(bot.start(TOKEN), compare_logfile(camera_path))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
