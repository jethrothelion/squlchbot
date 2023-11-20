import datetime
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
CHANNEL_ID=834800817042096131



intents = discord.Intents().all()

bot = discord.ext.commands.Bot(command_prefix = "!", intents=intents)

#socket connection
async def handle_client(client_socket):

    async def send_message(message):
        await loop.sock_sendall(client_socket, message.encode())
    global client
    client = client_socket
    print(time)
    password = "172362"

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
            channel = CHANNEL_ID
            channel = bot.get_channel(1146187982701875291)
            await channel.send(recieved)
    else:
        await send_message("gett outta here")


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

async def sendMessage(client, message):
    if message.__contains__("luna taking blinker"):
        x = 10
    else:
        await loop.sock_sendall(client, message.encode())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

    await bot.change_presence(activity=discord.Game(name="raconfeburgnite"))


#weawther a nd ti mwer systems
@aiocron.crontab("30 6 * * *")
async def WeatherTime():
    present = datetime.datetime.now()
    future = datetime.datetime(2023, 6, 17, 15, 0, 0)
    difference = future - present
    summer = str(difference)
    global totalsummer
    totalsummer = summer[:7]

    present2 = datetime.datetime.now()
    future2 = datetime.datetime(2024, 7, 9, 15, 0, 0)
    difference2 = future2 - present2
    cbray = str(difference2)
    global Cbray
    Cbray = cbray[:7]

    present4 = datetime.datetime.now()
    future4 = datetime.datetime(2024, 6, 29, 15, 0, 0)
    difference4 = future4 - present4
    gbray = str(difference4)
    global Gbray
    Gbray = gbray[:7]

    present3 = datetime.datetime.now()
    future3 = datetime.datetime(2024, 6, 17, 15, 0, 0)
    difference3 = future3 - present3
    rbray = str(difference3)
    global Rbray
    Rbray = rbray[:7]

    currentDayIndex = 12
    updateOccurred = False

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

    variable = "April 1 French Bread Pizza or Queso Pull Apart Sandwiches w/wo Salsa Assorted Cold Sandwiches Grape Tomatoes Fresh Orange Wedges April 4 Chicken Bites or French Toast Sticks w/ Sausage Assorted Cold Sandwiches Fresh Broccoli Craisins April 5 Cheese Steak Sandwich or Chicken and Green Chili Quesadilla Breakfast for Lunch Kits Baby Carrots Fresh Pear April 6 Bosco Sticks w/ Sauce or Ham and Cheese Melt Assorted Cold Sandwiches Celery Sticks Peaches April 7 Cheeseburger or Pepperoni and Cheese Calzone Breakfast for Lunch Kits Baby Carrots Strawberries April 8 Stuffed Crust Pizza or Chicken Quesadilla w/ Salsa Assorted Cold Sandwiches Grape Tomatoes Fresh Orange Wedges April 11 Chicken Tenders- Regular or Spicy Assorted Cold Sandwiches Fresh Broccoli Craisins April 12 EARLY DISMISSAL Grab and Go Lunches offered prior to dismissal April 13-15 April 18 NO SCHOOL April 19 Taco and Cheese Bowls w/ Scoops or Bean and Cheese Burrito Breakfast for Lunch Kits Baby Carrots Fresh Pear April 20 Bosco Sticks w/ Sauce or Egg and Cheese Taco Wrap Assorted Cold Sandwich Celery Sticks Peaches April 21 Cheeseburger or Pepperoni and Cheese Calzone Breakfast for Lunch Kits Baby Carrots Strawberries April 22 French Bread Pizza Or Pork Roll Sandwich w/ Cheese Assorted Cold Sandwich Grape Tomatoes Fresh Orange Wedges April 25 Chicken Tenders- Regular or Spicy Assorted Cold Sandwiches Fresh Broccoli Craisins April 26 Spicy Breaded Chicken Sandwich or Grilled Chicken Sandwich Breakfast for Lunch Kits Baby Carrots Applesauce April 27 Mozzarella Sticks w/wo Sauce or Beef Taco Assorted Cold Sandwiches Celery Sticks Peaches April 28 Breaded Chicken Sandwich or Garlic Pull Apart Sandwiches w/wo Sauce Breakfast for Lunch Kits Baby Carrots Strawberries April 29 French Bread Pizza or Queso Pull Apart Sandwiches w/wo Salsa Assorted Cold Sandwiches Grape Tomatoes Fresh Orange Wedges"
    words = variable.split("April")

    weather = (
                "Good morning todays forecast is " + e2.text + "\n a tempeture of " + e.text + " and a high off " + e32 + "\n")

    timedate = ("rn it is " + current_time + " todays date is " + todaystr)

    daystr = str(daySlot)

    if words[currentDayIndex].__contains__(daystr):
        lunch2 = ("todays lunch menu is " + words[currentDayIndex])
    else:
        lunch = "no lunch today lol"
    fullthing = weather + timedate
    extra = "thiswork"
    channel = bot.get_channel(1146187982701875291)
    await channel.send(fullthing)



async def on_guild_join(message, self, guild, member: discord.Member):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel)
    if user_message.__contains__("755069362418745385"):
        await member.ban(reason="reason")
        await message.channel.send(f'User {member} has been kick')



@bot.event
async def on_reaction_add(reaction, user, channel):
    reactionstr=str(reaction)
    if reactionstr == "🗑️":
        def is_me(m):
            return m.author == "luna"

        deleted = await channel.purge(limit=100, check=is_me)
        await channel.send(f'Deleted {len(deleted)} message(s)')



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
    # Your existing message processing logic
    await bot.process_commands(message)

    try:
        await sendMessage(client, stripmsg)
    except Exception as e:
        x = 1

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


    if username != "luna taking blinker":
        if user_message.lower() == "hello":
            await message.channel.send(f"hello: {username}")
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
        if username.__contains__("ben"):
            await message.channel.send("you sure?")
            return
        channelstr = str(channel)
        if channelstr.__contains__("Direct Message"):
            await message.channel.send("skibidie toiliet centeral")
            return






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
