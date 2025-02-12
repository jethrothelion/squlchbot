import aiocron
import datetime
import requests
import BeautifulSoup
from UIonwakeup import indoctronated

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
