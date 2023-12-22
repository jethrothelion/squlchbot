
from tkinter import *
import customtkinter

def indoctronated():
    lable = customtkinter.CTkLabel(master=root, text="taken")
    lable.place(relx=0.5, rely=0.5, anchor=SW)
    print("ye")
    button.destroy()

customtkinter.set_appearance_mode("dark")
root = customtkinter.CTk()
root.geometry("1920x960")
button = customtkinter.CTkButton (master=root, text="meds?", command = indoctronated)
button.place(relx=0.5, rely=0.5, anchor=CENTER)
lable = customtkinter.CTkLabel(master=root, text_color= "pink", text= "today forecast be Faira tempeture of 30 Ftodays date is 2023-12-14")

lable.place(relx=0.4, rely=0.1, anchor="ne")
