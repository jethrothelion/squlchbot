import asyncio
import socket
from datetime import datetime
import os
from ip2geotools.databases.noncommercial import DbIpCity
import asyncio
from pathlib import Path
current_path = Path()
env_file = current_path / "env.txt"
global loop

if __name__ != "__main__":
    loop = asyncio.get_event_loop()

#env variable file keyying
env_data = {}
with open(env_file, "r") as file:
    for line in file:
        if not line.strip():
            continue
        # Split the line into key and value, stripping any leading or trailing whitespaces
        key, value = map(str.strip, line.split("="))
        env_data[key.lower()] = value


async def send_message(ipaddy, message):
    await loop.sock_sendall(ipaddy, message.encode())


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
        if ipstr.startswith("192"):
            temp = DbIpCity.get(ip[0], api_key='free')
            print("incorrect password attempt from " + ipstr + " " + temp.region + " " + temp.country + " recieved password: " + received_password)


            with open("connections.txt", "a") as connectlog:
                now = datetime.now()
                connectlog.write(now.strftime(now.strftime("%Y-%m-%d %H:%M:%S")) + f"\nwrong pass atempt {ipstr}" + " from " + temp.region + " " + temp.country + " " + received_password)




    client_socket.close()

async def start_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    port = 8383
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")


    while True:
        client_socket, client_address = await loop.sock_accept(server_socket)

        ip = client_socket.getpeername()
        ipstr = str(ip)
        if ipstr.startswith("192"):
            temp = DbIpCity.get(ip[0], api_key='free')

            print(f"Connection from " + " from " + temp.region + " " + temp.country)

            with open("connections.txt", "a") as connectlog:
                now = datetime.now()
                connectlog.write(now.strftime("%Y-%m-%d %H:%M:%S") + f"\nConnection from {client_address}" + " from " + temp.region + " " + temp.country)

        asyncio.create_task(handle_client(client_socket))

async def main():
    # Run bot start and log reading concurrently
    await asyncio.gather(start_server())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
