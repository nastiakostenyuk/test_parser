import requests
import logging
import bs4
import dateparser

from fake_useragent import UserAgent
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

url = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273"

headers = {"User-Agent": UserAgent().random}
session = requests.Session()
session.headers.update(headers)


def parse_block(adv_block) -> dict:
    date = adv_block.find("div", class_="location").find("span", class_="date-posted").text.strip()
    try:
        date_time = datetime.strptime(date, "%d/%m/%Y").strftime("%d-%m-%Y")
    except ValueError:
        dt = dateparser.parse(date)
        date_time = dt.strftime("%d-%m-%Y")
    advertisement = {
        "img": adv_block.find("div", class_="image").find("img").get("data-src"),
        "title": adv_block.find("div", class_="title").find("a", class_="title").text.strip(),
        "date": date_time,
        "location": adv_block.find("div", class_="location").find("span").text.strip(),
        "beds": ''.join(adv_block.find("div", class_="rental-info").find("span", class_="bedrooms").text.split()),
        "description": adv_block.find("div", class_="description").text.strip(),
        "price": adv_block.find("div", class_="info").find("div", class_="info-container").find("div", class_="price").text.strip(),
    }
    return advertisement


def parse(pages):
    for page in range(pages):
        response = session.get(url, params={"page": page+1}, headers={"x-requested-with": "XMLHttpRequest"})
        soup = bs4.BeautifulSoup(response.text, "lxml")
        news_block_list = soup.select(".search-item")
        current_list = list(map(parse_block, news_block_list))
        print(current_list)
