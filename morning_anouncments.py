import aiocron
import datetime
import requests
import pyautogui
from tkinter import *
import customtkinter


customtkinter.set_appearance_mode("dark")
root = customtkinter.CTk()
root.geometry("1920x960")
Button = customtkinter.CTkButton (master=root, text="meds?", command = indoctronated())
Button.place(relx=0.5, rely=0.5, anchor=CENTER)
lable = customtkinter.CTkLabel(master=root, text_color= "pink", text= "today forecast be Faira tempeture of 30 Ftodays date is 2023-12-14")
lable.place(relx=0.4, rely=0.1, anchor="ne")

def indoctronated():
    lable = customtkinter.CTkLabel(master=root, text="taken")
    lable.place(relx=0.5, rely=0.5, anchor=SW)
    print("ye")
    Button.destroy(root)


#weawther and ti mwer systems
@aiocron.crontab("00 6 * * *")
async def WeatherTime():

    present = datetime.now()
    future = datetime(2024, 6, 17, 15, 0, 0)
    difference = future - present
    summer = str(difference)
    global totalsummer
    totalsummer = summer[:7]

    URL = "https://forecast.weather.gov/MapClick.php?CityName=Hatboro&state=PA&site=PHI&lat=40.1775&lon=-75.1048#.YnVdK07MK1s"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    e = soup.find("p", class_="myforecast-current-lrg")
    e2 = soup.find("p", class_="myforecast-current")
    e3 = soup.find("p", class_="temp temp-high")
    e32 = e3.text[6:]

    today = datetime.today()

    todaystr = str(today)
    monthSlot = todaystr[5] + todaystr[6]
    daySlot = todaystr[8] + todaystr[9]

    weather = (
                "today forecast be " + e2.text + "a tempeture of " + e.text)

    timedate = ("todays date is " + todaystr)

    daystr = str(daySlot)

    fullthing = weather + timedate


    #uses mouse to wake up screen morning anouncments
    pyautogui.moveTo(None, 10)

    #ui screen to be shown
    indoctronated.root.mainloop()
    try:
        indoctronated.lable.configure(text=fullthing)
        return
    except Exception as e:
        estr = str(e)
        print("error: " + estr)
        return
    return
