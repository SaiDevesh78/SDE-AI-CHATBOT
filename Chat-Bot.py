import pymongo
import json
import requests
import socket
import platform
import inquirer
import pyfiglet
import os
import pyttsx3
#import speech_recognition as sr
#import datetime
import getpass
from python_email_validation import AbstractEmailValidation
from decouple import config
from requests import get
from time import sleep
from rich.console import Console
#from rich.progress import Progress
from rich import print
from rich.table import Table

Database_pass = config('DATABASE')
Email_check_api_key= config('EMAIL_CHECK_API_KEY')
Ip_geo_api_key = config('IP_GEO_API_KEY')
Phone_check_api_key = config('PHONE_CHECK_API_KEY')
Bot_name = "SDE AI ALPHA BOT"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice',voices[0].id)

client = pymongo.MongoClient(f"mongodb+srv://SDE-AI-Chat_Bot:{str(Database_pass)}@chat-bot-database.o5sj3pv.mongodb.net/?retryWrites=true&w=majority")
mydb = client["User-Database"]
mydb1 = client["Commands-Database"]
user_data = mydb["user-information"]
commands_data = mydb1["commands-information"]
console = Console()

os.system('cls')

'''with Progress() as progress:

    Start = progress.add_task("[bold yellow][*][red]Loading UI...", total=1000)
    Mid = progress.add_task("[bold yellow][*][green]Preparing assistant...", total=1000)
    End = progress.add_task("[bold yellow][*][cyan]Getting the Server...", total=1000)

    while not progress.finished:
        progress.update(Start, advance=2.9)
        progress.update(Mid, advance=2.7)
        progress.update(End, advance=2.8)
        sleep(0.02)
'''
os.system('cls')

ASCII_art_1 = pyfiglet.figlet_format(Bot_name,font="bubble")
console.print(f"[bold cyan]{ASCII_art_1}[/bold cyan]")
print()
def Computer_information():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    
    global public_ip
    
    try:
        public_ip = get("https://api.ipify.org").text
        Computer_information.public_ip = public_ip
    except Exception:
        Computer_information.public_ip = "Couldn't get Public IP Address"

    global processor_info ,OS_info ,mechine_info ,host_name, priv_ip
    
    processor_info = platform.processor()
    OS_info = platform.system()
    mechine_info = platform.machine()
    host_name = hostname
    priv_ip = IPAddr

  
def Email_check(Email):
    console = Console()
    while 1:
        api_key = str(Email_check_api_key)
        email_address = Email
        response = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={Email}")
        status = str(response.json()['is_valid_format'])
        Email1 = str(response.json())
        if status == str({"value": True,"text": "TRUE"}):
            global checked_email
            checked_email = str(Email1)
            break
        elif status == str({"value": False,"text": "FALSE"}):
            Email = console.input("[bold red][-][/bold red]That email seems to be invalid plese re-enter a valid one: ")
        else:
            checked_email = "NOT CHECKED\n"+str(Email1)
            break


def Geo_location_IP():
    Computer_information()
    YOUR_GEOLOCATION_KEY = str(Ip_geo_api_key)
    ip_address = public_ip
    response = requests.get('https://ipgeolocation.abstractapi.com/v1/?api_key=' + YOUR_GEOLOCATION_KEY + '&ip_address=' + ip_address)
    global result
    result = json.loads(response.content)


def Phone_number_check(Phone_number):
    while 1:
        Phone_number_count = len(str(Phone_Number))
        if Phone_number_count == 10:
            break
        else:
            Phone_Number = int(console.input("[bold red][-][/bold red]That number seems to have more/less numbers than usual re-enter a valid one: "))
    response = requests.get(f"https://phonevalidation.abstractapi.com/v1/?api_key={str(Phone_check_api_key)}={Phone_number}")
    global checked_phone_number
    checked_phone_number = str(response.content).replace(",",",\n")


def New_user():
    console = Console()
    counter = 0
    for x in user_data.find({},{"_id": 1}):
        counter = counter+1
    counter = counter+1

    console.print("[bold yellow][*][/bold yellow]Plese try answering all for the assistant to work properly")
    
    _id = f"User {counter}"
    Name = console.input("[bold cyan][+][/bold cyan]Whats your name (This will be used for logins in the future)?: ")
    Password = console.input("[bold cyan][+][/bold cyan]Whats the password you want to set (This will be used for logins in the future)?: ")
    console.print("[bold cyan][+][/bold cyan]Whats your gender?")
    sleep(1)
    questions = [
    inquirer.List(
        "gender",
        message="whats your gender?",
        choices= ["Male", "Female", "Transgender", "Non-binary/non-conforming", "Prefer not to respond"],),]
    Gender = str(inquirer.prompt(questions))
    
    DOB = console.input("[bold cyan][+][/bold cyan]Whats your Date of Birth (add a - after year, month and day)?: ")
    Phone_Number = int(console.input("[bold cyan][+][/bold cyan]Whats your phone number?: "))
    Email = console.input("[bold cyan][+][/bold cyan]Whats your email?: ")

    Phone_number_check(Phone_Number)
    Email_check(Email)
    Computer_information()
    Geo_location_IP()
    
    global new_userdata

    new_userdata = {
                    "_id": _id,
                    "IP": priv_ip,
                    "Name": Name,
                    "Password": Password,
                    "Gender": Gender,
                    "DOB": DOB,
                    "Address": result,
                    "Phone Number": checked_phone_number,
                    "Email": checked_email,
                    "System Information":{
                        "Processor":processor_info,
                        "OS":OS_info,
                        "Mechine":mechine_info,
                        "Hostname":host_name,
                        "Public IP":public_ip
}
}
    while True:
        os.system('cls')
        table = Table(title="Your Info")

        table.add_column("No.", justify="center", style="cyan")
        table.add_column("Key", justify="center",style="magenta")
        table.add_column("Value", justify="center", style="green")

        table.add_row("1", "Name", Name)
        table.add_row("2", "Password", Password)
        table.add_row("3", "Gender", Gender)
        table.add_row("4", "Date of Birth", DOB)
        table.add_row("5", "Phone Number", Phone_Number)
        table.add_row("6", "Email", Email)

        console = Console()
        console.print(table)
        
        data_correct_or_not = console.input("[bold cyan][+][/bold cyan]Is the above give information right?(y/n): ")
        if data_correct_or_not == "y":
            break
        
        elif data_correct_or_not == "n":
            wrong_data = int(console.input("[bold yellow][?][/bold yellow]Which one of them is the wrong one (plese enter just the number): "))
            if wrong_data == 1:
                wrong_fix = console.input("[bold red][-][/bold red]Plese re-enter the right Name: ")
                new_userdata["Name"] = wrong_fix
                Name = wrong_fix
            elif wrong_data == 2:
                wrong_fix = console.input("[bold red][-][/bold red]Plese re-enter the right Password: ")
                new_userdata["Password"] = wrong_fix
                Password = wrong_fix
            elif wrong_data == 3:
                console.print("[bold red][-][/bold red]Plese re-select your correct gender?")
                sleep(1)
                questions = [
                inquirer.List(
                    "gender",
                    message="whats your gender?",
                    choices= ["Male", "Female", "Transgender", "Non-binary/non-conforming", "Prefer not to respond"],),]
                wrong_fix = str(inquirer.prompt(questions))
                new_userdata["Gender"] = wrong_fix
                Gender = wrong_fix
                
            elif wrong_data == 4:
                wrong_fix = console.input("[bold red][-][/bold red]Plese re-enter your Date of Birth (add a - after year, month and day)?: ")
                new_userdata["DOB"] = wrong_fix
                DOB = wrong_fix
                   
            elif wrong_data == 5:
                Phone_Number = int(console.input("[bold red][-][/bold red]Plese re-enter the right phone number?: "))
                Phone_Number = "+91"+str(Phone_Number)
                Phone_number_check(Phone_Number)
                new_userdata["Phone Number"] = checked_phone_number
                
            elif wrong_data == 6:
                Email = console.input("[bold red][-][/bold red] Plese re-enter your email: ")
                Email_check(Email)
                new_userdata["Email"] = checked_email
                
    console = Console()
    tasks = ["Name","Password","Gender","DOB","Phone number","Email"]
    with console.status("[bold green]Uploading Data to the Database...") as status:
        while tasks:
            task = tasks.pop(0)
            sleep(1)
            console.log(f"{task} Uploaded")

    user_data.insert_one(new_userdata)  
    os.system('cls')


def User_not_found():
    print("[bold red][-][/bold red]Hey we are not finding you in our database are you using a diffrent system or network?")
    new_old_user = console.input("[bold yellow][?][/bold yellow]Are you a new user (y/n)?: ")
    os.system("cls")
    if new_old_user in ['n', 'N']:
        User_name = getpass.getpass(prompt="Whats your User Name?: ")
        User_Passowrd = getpass.getpass(prompt="Whats your User Password?: ")
        os.system("cls")
        counter = 0
        for x in user_data.find({},{"_id":1 , "Name":1, "Password":1}):
            counter = counter+1
            counter1 = f"User {counter}"
            Info_dict = {"_id":counter1,"Name":User_name, "Password":User_Passowrd}
            if Info_dict == x:
                print("[bold green]Logging you in.......")
                break
            else:
                print("Hey it seems there is no account like that")
                while True:
                    new_old_user1 = console.input("[bold yellow][?][/bold yellow]Are you sure you are not a new user (y/n)?: ")
                    if new_old_user1 in ['y', 'Y']:
                        os.system("cls")
                        User_name = getpass.getpass(prompt="Whats your User Name?: ")
                        User_Passowrd = getpass.getpass(prompt="Whats your User Password?: ")
                        os.system("cls")
                        counter = 0
                        for x in user_data.find({},{"_id":1 , "Name":1, "Password":1}):
                            counter = counter+1
                            counter1 = f"User {counter}"
                            Info_dict = {"_id":counter1,"Name":User_name, "Password":User_Passowrd}
                            if Info_dict == x:
                                print("[bold green]Logging you in.......")
                                break
                            break
                        break
                    elif new_old_user1 in ['n', 'N']:
                        New_user()                      
    elif new_old_user in ['y', 'Y']:
        New_user()
        

Computer_information()
counter = 0

for x in user_data.find({},{"_id":1 , "IP":1, "System Information":{"Hostname":1}}):
    counter = counter+1
    counter1 = f"User {counter}"
    Info_dict = {"_id":counter1,"IP":priv_ip, "System Information":{"Hostname":host_name}}
    if Info_dict == x:
        User_number = counter1
        break
    elif list(Info_dict) not in list(x):
        User_not_found()