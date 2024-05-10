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


#socket connection ip texting
async def handle_client(client_socket):

    async def send_message(message):
        await loop.sock_sendall(client_socket, message.encode())


    global client
    client = client_socket

    print(datetime.now())


    password = env_data.get("ip password")

    # Send a prompt for password
    await send_message("Enter password: ")

    data = await loop.sock_recv(client_socket, 1024)
    datastr = str(data.decode().strip())
    received_password = datastr

    # Check the received password
    if received_password == password:
        await send_message("Access granted. Welcome!\n")

        while True:
            data = await loop.sock_recv(client_socket, 1024)
            if not data:
                break

            print(f"{data.decode('utf-8')}")


            recieved = data.decode()
            channelpart = recieved.split(" ")


            if channelpart.__contains__("shit"):
                channel = bot.get_channel(837553172217593906)
                await channel.send(recieved[4:])
            if channelpart.__contains__("shop"):
                channel = bot.get_channel(1174870748142256188)
                await channel.send(recieved[4:])
            if channelpart.__contains__("plan"):
                channel = bot.get_channel(1174871457701056593)
                await channel.send(recieved[4:])
            if channelpart.__contains__("resume"):
                channel = bot.get_channel(1176520850678226964)
                await channel.send(recieved[6:])
            if channelpart.__contains__("fart"):
                channel = bot.get_channel(1185829928088903710)
                await channel.send(recieved[4:])


    else:
        await send_message("gett outta here")
        ip = client.getpeername()
        ipstr = str(ip)
        temp = DbIpCity.get(ip[0], api_key='free')
        print("incorrect password attempt from " + ipstr + " " + temp.region + " " + temp.country + " recieved password: " + received_password)


        with open("connections.txt", "a") as connectlog:
            now = datetime.now()
            connectlog.write(now.strftime(now.strftime("%Y-%m-%d %H:%M:%S")) + f"\nwrong pass atempt {ipstr}" + " from " + temp.region + " " + temp.country + " " + received_password)




    client_socket.close()

async def start_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.68.65"
    port = 8383

    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = await loop.sock_accept(server_socket)

        ip = client_socket.getpeername()
        ipstr = str(ip)
        temp = DbIpCity.get(ip[0], api_key='free')

        print(f"Connection from " + " from " + temp.region + " " + temp.country)

        with open("connections.txt", "a") as connectlog:
            now = datetime.now()
            connectlog.write(now.strftime("%Y-%m-%d %H:%M:%S") + f"\nConnection from {client_address}" + " from " + temp.region + " " + temp.country)

        asyncio.create_task(handle_client(client_socket))


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

    await bot.change_presence(activity=discord.Game(name="raconfeburgnite"))
    discord.opus.load_opus(r"C:\Users\Corey\Downloads\libopus-0.x64.dll")
    print('hewo')

#weawther a nd ti mwer systems
@aiocron.crontab("00 6 * * *")
async def WeatherTime():

    present = datetime.now()
    future = datetime(2024, 6, 17, 15, 0, 0)
    difference = future - present
    summer = str(difference)
    global totalsummer
    totalsummer = summer[:7]

    currentDayIndex = 12

    URL = "https://forecast.weather.gov/MapClick.php?CityName=Hatboro&state=PA&site=PHI&lat=40.1775&lon=-75.1048#.YnVdK07MK1s"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    e = soup.find("p", class_="myforecast-current-lrg")
    e2 = soup.find("p", class_="myforecast-current")
    e3 = soup.find("p", class_="temp temp-high")
    e32 = e3.text[6:]

    today = date.today()

    todaystr = str(today)
    monthSlot = todaystr[5] + todaystr[6]
    daySlot = todaystr[8] + todaystr[9]

    weather = (
                "today forecast be " + e2.text + "a tempeture of " + e.text)

    timedate = ("todays date is " + todaystr)

    daystr = str(daySlot)

    fullthing = weather + timedate
    extra = "thiswork"
    channel = bot.get_channel(1146187982701875291)
    msg = await channel.send(fullthing)
    await msg.add_reaction("💊")

    #uses mouse to wake up screen morning anouncments
    pyautogui.moveTo(None, 10)

    #ui screen to be shown
    UIonwakeup.root.mainloop()
    try:
        UIonwakeup.lable.configure(text=fullthing)
        return
    except Exception as e:
        estr = str(e)
        print("error: " + estr)
        return
    return


async def on_guild_join(message, self, guild, member: discord.Member):
    if member.__contains__("755069362418745385"):
        await member.ban(reason="reason")
        await message.channel.send(f'User {member} has been kick')



@bot.event
async def on_reaction_add(reaction, user, channel):
    print("reaction added" + reaction + user + channel)

async def send_message(ipaddy, message):
    await loop.sock_sendall(ipaddy, message.encode())


@bot.event
async def on_message(message, user: discord.Member = None):

    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel)
    print(f"{username}: {user_message} ({channel})")
    user_message = str(message.content)
    user = message.author

    stripmsg = channel + " " + username + " " + user_message

    await bot.process_commands(message)

    #reminder trxt system
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
                await message.channel.send(Cbray + "till Coreys birthday" + "\n" + Rbray + "till ryleis birthday" + "\n" + Gbray + "till gs brithday" + "\n")

    if user_message.__contains__("todays forecast is"):
        med="💊"
        await message.add_reaction(med)
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
                os.system(f'C:\\Users\\Corey\\Downloads\\yt-dlp.exe "ytsearch:{search}" {opts}')
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
        if user_message.__contains__("bbl"):
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
    await asyncio.gather(bot.start(TOKEN), compare_logfile(camera_path), start_server())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
