import datetime
from datetime import datetime
import discord
import random
from discord.ext import tasks, commands
import aiocron
import time
from datetime import date
import requests
from bs4 import BeautifulSoup
import asyncio
import socket
import youtube_dl
import UIonwakeup
from ip2geotools.databases.noncommercial import DbIpCity
CHANNEL_ID=834800817042096131

intents = discord.Intents().all()

bot = discord.ext.commands.Bot(command_prefix = "!", intents=intents)
async def temp():
    channel = bot.get_channel(1186067959479812126)
    await channel.send("detected")


#socket connection
async def handle_client(client_socket):

    async def send_message(message):
        await loop.sock_sendall(client_socket, message.encode())


    global client
    client = client_socket

    print(datetime.now())
    password = "skibiditoilet433"

    # Send a prompt for password
    await send_message("Enter password: ")

    data = await loop.sock_recv(client_socket, 1024)
    received_password = data.decode().strip()

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
            if channelpart.__contains__("mom"):
                channel = bot.get_channel(1105226246633304235)
                await channel.send(recieved[3:])


    else:
        await send_message("gett outta here")
        ip = client.getpeername()
        ipstr = str(ip)
        temp = DbIpCity.get(ip[0], api_key='free')
        print("incorrect password attempt from " + ipstr + " " + temp.region + " " + temp.country)




    client_socket.close()

async def start_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "0.0.0.0"
    port = 8383

    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = await loop.sock_accept(server_socket)
        print(f"Connection from {client_address}")

        asyncio.create_task(handle_client(client_socket))


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

    await bot.change_presence(activity=discord.Game(name="raconfeburgnite"))


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

    t = time.localtime()
    current_time = time.strftime("%I:%M:%S", t)
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

    UIonwakeup.root.mainloop()
    try:
        UIonwakeup.lable.configure(text=fullthing)
    except e:
        print("error: " + e)





async def on_guild_join(message, self, guild, member: discord.Member):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel)
    if user_message.__contains__("755069362418745385"):
        await member.ban(reason="reason")
        await message.channel.send(f'User {member} has been kick')



@bot.event
async def on_reaction_add(reaction, user, channel):
    print("reaction added" + reaction + user + channel)

async def send_message(ipaddy, message):
    print(message)
    await loop.sock_sendall(ipaddy, message.encode())



@bot.event
async def on_message(message, user: discord.Member = None):




    messagestr = str(message)
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel)
    print(f"{username}: {user_message} ({channel})")
    user_message = str(message.content)
    user = message.author
    user2 = str(user)


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


    if username != bot.user.name:



       ## if user_message.__contains__("purge"):
        ##    print("ehel")
        ##    user_message[:6] = num
        ##    int(num)
         ##   print("he")
#
          ##  return
        if user_message.lower() == "hello":
            await message.channel.send(f"hello {username}")
            return
        if user_message.lower() == "bye":
            await message.channel.send("goodbye")
            return
        if user_message.lower() == "random":
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
            await message.channel.send("skiltles -")
            return
        await send_message(client, stripmsg)



@bot.event
async def on_message_edit(before, after):
    print(
        f"{before.author}edit a message. \n"
        f"before: {before.content}\n"
        f"after: {after.content}"
    )


TOKEN = "OTY2NDQ4NTk5Mjg4NDAxOTkw.YmB5ZQ.io3Yvn5cqPtST1SXQreLM12hRX4"
async def main():
    await bot.start(TOKEN)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    # Run the bot and server concurrently using asyncio.gather
    tasks = [main(), start_server()]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.run_forever()
