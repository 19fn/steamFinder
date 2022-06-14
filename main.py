import requests, signal, re
import mysql.connector
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep

HEADER = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
# Cambiar URL
URL = "https://store.steampowered.com/app/1402320/Medal_of_Honor_Above_and_Beyond/"
# Cambiar Nombre
GAME = "Medal of honor Above and Beyond".upper()

mydb = mysql.connector.connect( host="172.24.35.232",
                                user="admin",
                                password="SteamFinder2022",
                                database="steamfinder_db")
mycursor = mydb.cursor()

def ctrl_c(sig, frame):
    print("\n[!] Se presionó (ctrl_c) saliendo...")
    exit()
signal.signal(signal.SIGINT, ctrl_c)

def getPrice():
    page = requests.get(URL, headers=HEADER)
    soup = BeautifulSoup(page.content, "lxml")
    get_price = soup.find("div", {"class" : "game_purchase_action"})
    if get_price:
        price = get_price.get_text()
        price = price.strip()
        price = re.findall('(?:\d+\.)?\d+,\d+', price)
        format_price = price[0].replace(".","")
        final_price = format_price.replace(",",".")
    return final_price

def loadPrice(price):
    # Getting the current date and time
    dt = datetime.now()
    sql = "INSERT INTO Price (game, price, date) VALUES (%s, %s, %s)"
    val = (f"{GAME}", f"{price}", f"{dt}")
    mycursor.execute(sql, val)
    mydb.commit()
    return print("Price added to database.")

def minPrice():
    sql = f"SELECT MIN(price) as min_price from Price WHERE game = '{GAME}'"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    return myresult[0]

def main():
    try:
        loadPrice(getPrice())
    except ConnectionError:
        print("[!] Error connecting to database.")
        exit
    while(True):
        print(f"\n[*] Buscando cambios en el precio de: '{GAME}'")
        new_price = getPrice()
        old_price = minPrice()
        print(float(old_price))
        if float(new_price) == float(old_price):
            print("[+] Price has no changed.")
        elif float(new_price) < float(old_price):
            print(f"[+] Price has changed and now is: ${new_price} ARS")
        sleep(5) 

if __name__ == "__main__":
    main()
    #print(getPrice())
    #loadPrice(getPrice())
    #print(minPrice())
