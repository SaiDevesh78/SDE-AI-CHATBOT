from os import environ
import pymongo
import json
import requests
import socket
import platform
import inquirer
from decouple import config
from requests import get
from time import sleep
from rich.console import Console
from rich.progress import Progress
from rich import print
from rich.table import Table

Database_pass = config('DATABASE')
Email_check_api_key= config('EMAIL_CHECK_API_KEY')
Ip_geo_api_key = config('IP_GEO_API_KEY')
Phone_check_api_key = config('PHONE_CHECK_API_KEY')

client = pymongo.MongoClient(f"mongodb+srv://SDE-AI-Chat_Bot:{str(Database_pass)}@chat-bot-database.o5sj3pv.mongodb.net/?retryWrites=true&w=majority")
mydb = client["User-Database"]
mydb1 = client["Commands-Database"]
user_data = mydb["user-information"]
commands_data = mydb1["commands-information"]


with Progress() as progress:

    Start = progress.add_task("[red]Loading UI...", total=1000)
    Mid = progress.add_task("[green]Downloading Packages...", total=1000)
    End = progress.add_task("[cyan]Getting Database...", total=1000)

    while not progress.finished:
        progress.update(Start, advance=1.6)
        progress.update(Mid, advance=1.4)
        progress.update(End, advance=1.5)
        sleep(0.02)

        
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
    while 1:
        api_key = str(Email_check_api_key)
        email_address = Email
        response = requests.get("https://isitarealemail.com/api/email/validate",
            params = {'email': email_address},
            headers = {'Authorization': "Bearer " + api_key })

        status = response.json()['status']
        if status == "valid":
            global checked_email
            checked_email = Email
            break
        elif status == "invalid":
            Email = input("Hmm.. That email seems to be invalid plese re-enter a valid one: ")
        else:
            checked_email = Email+" Not varified"
            break


def Geo_location_IP():
    Computer_information()
    YOUR_GEOLOCATION_KEY = str(Ip_geo_api_key)
    ip_address = public_ip
    response = requests.get('https://ipgeolocation.abstractapi.com/v1/?api_key=' + YOUR_GEOLOCATION_KEY + '&ip_address=' + ip_address)
    global result
    result = json.loads(response.content)

def Phone_number_check(Phone_number):
    response = requests.get(f"https://phonevalidation.abstractapi.com/v1/?api_key={str(Phone_check_api_key)}={Phone_number}")
    global checked_phone_number
    checked_phone_number = response.content


def New_user():
    counter = 0
    for x in user_data.find({},{"_id": 1}):
        counter = counter+1
    counter = counter+1

    print("[*]Plese try answering all for the assistant to work properly")
    
    _id = f"User {counter}"
    Name = input("[+]Whats your name?: ")
    questions = [
    inquirer.List(
        "Gender",
        message= "Whats your gender?",
        choices= ["Male", "Female", "Transgender", "Non-binary/non-conforming", "Prefer not to respond"],),]
    Gender = str(inquirer.prompt(questions))
    DOB = input("[+]Whats your Date of Birth(add a / after year, month and day)?: ")
    Phone_Number = int(input("[+]Whats your phone number?: "))
    Phone_Number = "+91"+str(Phone_Number)
    Email = input("[+]Whats your email?: ")

    Phone_number_check(Phone_Number)
    Email_check(Email)
    Computer_information()
    Geo_location_IP()
    
    global new_userdata

    new_userdata = {
                    "_id": _id,
                    "IP": priv_ip,
                    "Name": Name,
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
    while 1:
        table = Table(title="Your Info")

        table.add_column("No.", justify="center", style="cyan")
        table.add_column("Key", justify="center",style="magenta")
        table.add_column("Value", justify="center", style="green")

        table.add_row("1", "Name", Name)
        table.add_row("2", "Gender", Gender)
        table.add_row("3", "Date of Birth", DOB)
        table.add_row("4", "Phone Number", Phone_Number)
        table.add_row("5", "Email", checked_email)

        console = Console()
        console.print(table)
        
        new_user_data_correct_or_not = input("Is the above give information right?(y/n): ").lower
        if new_user_data_correct_or_not == "y":
            break
        else:
            wrong_data = int(input("Which one of them is the wrong one(plese enter just the number): "))
            if wrong_data == 1:
                wrong_fix = input("Plese re-enter the right Name: ")
                new_userdata["Name"] = wrong_fix

New_user()

console = Console()
tasks = ["Name","Gender","DOB","Address","Phone number","Email","System information"]
with console.status("[bold green]Uploading Data to the Database...") as status:
    while tasks:
        task = tasks.pop(0)
        sleep(1)
        console.log(f"{task} Uploaded")