import requests, re
from bs4 import BeautifulSoup as bs4

HEADER = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}

def getPrice(url, header=HEADER):
    page = requests.get(url, headers=header)
    soup = bs4(page.content, "lxml")
    get_price = soup.find("div", {"class" : "game_purchase_price price"})
    if get_price != None:
        price = re.findall('(?:\d+\.)?\d+,\d+', str(get_price))
        price = price[0].replace(".","")
        price = price.replace(",",".")
    else:
        price = False
    return price