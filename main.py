from lxml import html
import requests
import urllib.request
import json
import re
from bs4 import BeautifulSoup

def get_source(page_url):
   r = requests.get(page_url)
   source = html.fromstring(r.content)
   return source

#shitty_string = "data.result.status === '0' && data.result.price"
#def get_availability(source):
#   div = source.xpath("//div[contains(@ng-show, shitty_string)][contains(@class, 'ng-hide')]")
#   a = source.xpath("//a[contains(@class, 'yacht-price-box-reservation disabled')]")[0]
#   return a

def get_price(source):
   price = source.xpath("//meta[contains(@itemprop, 'price')]/@content")[0]
   return price

page_template = "https://www.yachtic.com/yacht-name?d=date.2022&w=1"

date_file = open("dates", "r")
dates = date_file.readlines()

yacht_file = open("yacht-names", "r")
yachts = yacht_file.readlines()

result_file = open("result", "w")

#main thing
for yacht in yachts:
   result_file.write(yacht)
   page_yacht_template = page_template.replace("yacht-name", yacht.translate(str.maketrans('', '', ' \n\t\r')))
   for date in dates:
      result_file.write(date)
      page = page_yacht_template.replace("date", date.translate(str.maketrans('', '', ' \n\t\r')))
      source = get_source(page)
      price = get_price(source)
      result_file.write(price)
      result_file.write("\n\n")
   result_file.write("\n")
