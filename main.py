import requests, signal, re, os
import mysql.connector
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep

HEADER = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
# Cambiar URL
URL = "https://store.steampowered.com/app/1402320/Medal_of_Honor_Above_and_Beyond/"
# Cambiar Nombre
GAME = "Medal of honor Above and Beyond".upper()

mydb = mysql.connector.connect( host="172.18.25.8",
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

def minPrice():
    sql = f"SELECT MIN(price) as min_price from Price WHERE game = '{GAME}'"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    return myresult[0]

def main():
    try:
        while(True):
            loadPrice(getPrice())
            print(f"\n[*] Searching changes in game price: '{GAME}'")
            new_price = getPrice()
            old_price = minPrice()
            price_list = []
            price_list.extend([float(new_price),float(old_price)])
            price_list.sort()
            if float(new_price) == float(price_list[0]):
                print("[+] Price has no changed.", end="", flush=True)
            elif float(price_list[0]) < float(new_price):
                print(f"[+] Price has changed and now is: ${old_price} ARS", end="", flush=True)
                break
            sleep(60)
            os.system('cls')
    except ConnectionError:
        print("[!] Error connecting to database.")
        exit

if __name__ == "__main__":
    main()
