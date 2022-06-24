import requests, re
from bs4 import BeautifulSoup

global final_price
HEADER = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}

def getPrice(url,header=HEADER):
    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.content, "lxml")
    get_price = soup.find("div", {"class" : "game_purchase_action"})
    if get_price:
        price = get_price.get_text()
        price = price.strip()
        price = re.findall('(?:\d+\.)?\d+,\d+', price)
        format_price = price[0].replace(".","")
        final_price = format_price.replace(",",".")
    return final_price