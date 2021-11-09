import requests, signal, smtplib
from email.message import EmailMessage
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep

HEADER = {"User-Agent" : "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
# Cambiar URL
URL = "https://store.steampowered.com/app/768520/Red_Solstice_2_Survivors/"
# Cambiar Nombre
GAME = "red solstice 2 survivors".upper()

def ctrl_c(sig, frame):
    print("\n[!] Se presionó (ctrl_c) saliendo...")
    exit()
signal.signal(signal.SIGINT, ctrl_c)

def mailTo(msg):
    mail = EmailMessage()
    mail.set_content(f"{msg}")
    mail["Subject"] = f"{GAME} - STEAM"
    mail["From"] = "xxxxxxx@gmail.com"
    mail["To"] = "xxxxxxx@gmail.com"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("xxxxxx@gmail.com", "XXXXXX")
    server.send_message(mail)
    server.quit()

def getPrice():
    page = requests.get(URL, headers=HEADER)
    soup = BeautifulSoup(page.content, "lxml")
    get_price = soup.find("div", {"class" : "game_purchase_price price"})
    get_desc_price = soup.find("div", {"class" : "discount_final_price"})
    if get_desc_price:
        get_dsc_price = get_desc_price.get_text()
        desc_price = get_dsc_price.strip()
        desc_price = desc_price[5:]
        desc_price = desc_price.replace(".","")
        desc_price = desc_price.replace(",",".")
        return desc_price
    if get_price:
        get_price = get_price.get_text()
        price = get_price.strip()
        price = price[5:]
        price = price.replace(".","")
        price = price.replace(",",".")
        return get_price

def readFile():
    file = open("price.txt", "r")
    if file.mode == "r":
        price = file.read()
    file.close
    return price

def writeFile(price):
    file = open("price.txt", "w")
    if file.mode == "w":
        file.write(price)
    file.close

def main():
    try:
        open("price.txt")
    except FileNotFoundError:
        writeFile(getPrice())
    while(True):
        print(f"\n[*] Buscando cambios en el precio de: '{GAME}'")
        old_price = readFile()
        new_price = getPrice()
        if float(new_price) < float(old_price):
            msg = f"[ ! ] El precio de '{GAME}' ha bajado: " + "\n[+] Precio anterior: ARS$ " + str(old_price) + "\n[+] Precio ACTUAL: ARS$ " + str(new_price) + "\n" + "[+] URL: " + str(URL)
            mailTo(msg)
            hora = str(datetime.today().hour)+":"+str(datetime.today().minute)
            print(f"\n[*] El precio de '{GAME}' ha bajado. \n[+] Email enviado a: xxxxxxxxxxxx@gmail.com \n[+] Hora: {hora}")
        sleep(7200) 

if __name__ == "__main__":
    main()
