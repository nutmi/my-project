from bs4 import BeautifulSoup
import requests
import time
from getuseragent import UserAgent
import random
import os
import datetime
from logger import setup_logging


loger = setup_logging("log")
useragent = UserAgent()


# url of a product
URL = ""

# notification settings
NOTIFICATION_URL = ""
USER_TOKEN = ""
API_KEY = ""


PROXY_URL_LIST = []

# hours when not to work
LST_OF_HOURS = [21, 22, 23, 1, 2, 3, 4, 5]

# agent = useragent.Random()


def check_ip(proxy):
    r = requests.get("https://api.ipify.org?format=json", proxies=proxy)
    return r.json()["ip"]


def sent_notification(text):
    myobj = {"token": API_KEY, "user": USER_TOKEN, "message": text}
    r = requests.post(NOTIFICATION_URL, json=myobj)
    print(r.content)


# myuseragent = UserAgent("all", requestsPrefix=True).Random()
# print(myuseragent)
# data = requests.get(url)
# print(data.content)
# list_of_ids = []
# soup = BeautifulSoup(data.content, "html.parser")
# def get_html_body(url, agent):rasberry piorange pi
#     with sync_playwright() as p:
#         # Launch a browser
#         browser = p.chromium.launch(headless=False)

#         # Open a new page
#         context = browser.new_context(user_agent=agent)

#         # Create a new page within the context
#         page = context.new_page()

#         # Navigate to the URL
#         page.goto(url)

#         # Extract the body of the HTML
#         html_body = page.content()

#         # Close the browser
#         time.sleep(20)
#         browser.close()

#         return html_body


# body = get_html_body(url, agent)
# print(body)
# driver = uc.Chrome(headless=True, use_subprocess=True)
# print(driver.get(url))


def extract(mp, data):

    soup = BeautifulSoup(data.content, "html.parser")
    found_items = soup.find_all("li", class_="EntityList-item")
    for li in found_items:

        # get name of a product
        link = li.find("a")
        # time = li.find("div", class_="entity-pub-date")
        if link:
            #     print(link["name"])
            # list_of_ids.append(link["name"])

            # get id of a product
            mp[link["name"]] = link.text
    return mp


def main():

    # currently last item in a shop
    last_item = "13988950"

    # get rendom proxy from a list
    proxy = {
        "http": PROXY_URL_LIST[0],
        "https": PROXY_URL_LIST[0],
        # "https": "https://101.66.199.247:8085",
        # "https": "socks5://168.205.217.41:4145",  # Replace with your HTTP proxy
        # Replace with your HTTP proxy
        # "https": "https://152.53.36.109:33069",  # Replace with your HTTPS proxy
    }

    # check for current ip
    checked_ip = check_ip(proxy)
    if checked_ip == "146.212.195.7":
        loger.error("proxy is the same as servers")
        os._exit(0)

    print(checked_ip)
    while True:

        list_of_ids = {}

        # user agent
        myuseragent = UserAgent("all", requestsPrefix=True).Random()
        # print(myuseragent)

        # get data

        current_time = int(time.ctime()[10:13])

        if current_time not in LST_OF_HOURS:

            checked_ip = check_ip(proxy)
            if "146.212.195.7" == "146.212.195.7":
                loger.error("proxy is the same as servers")
                os._exit(0)

            data = requests.get(URL, headers=myuseragent, proxies=proxy)

            # go throught all items
            list_of_ids = extract(list_of_ids, data)

            # it may be a captcha
            # list_of_ids = []
            try:
                if list(list_of_ids.keys())[0] != last_item:

                    # print("not the same")
                    # print(f"new item: {list_of_ids[list(list_of_ids.keys())[0]]}")

                    loger.info(f"new item: {list_of_ids[list(list_of_ids.keys())[0]]}")

                    last_item = list(list_of_ids.keys())[0]

                    sent_notification(list_of_ids[list(list_of_ids.keys())[0]])
                else:
                    # print("last item is the same")
                    loger.info("last item is the same")
            except:

                loger.error("probably captcha")
                print("probably captcha")
                random_proxy = random.choice(PROXY_URL_LIST)
                proxy["http"] = random_proxy
                proxy["https"] = random_proxy
                print(check_ip(proxy))
                # print(soup.prettify())
            print(list_of_ids)

        else:
            print("current hours not")
            loger.info("currently sleep hours")
        time.sleep(600)


proxy = {
    "http": PROXY_URL_LIST[0],
    "https": PROXY_URL_LIST[0],
    # "https": "https://101.66.199.247:8085",
    # "https": "socks5://168.205.217.41:4145",  # Replace with your HTTP proxy
    # Replace with your HTTP proxy
    # "https": "https://152.53.36.109:33069",  # Replace with your HTTPS proxy
}
# print(proxy)
# check_ip()
# random_proxy = random.choice(PROXY_URL_LIST)
# proxy["http"] = random_proxy
# proxy["https"] = random_proxy
# print(proxy)
# print(time.ctime()[10:13])
# lst_of_hours = [22, 23, 0, 1, 2, 3, 4, 5, 6]
# if int(time.ctime()[10:13]) in lst_of_hours:
#     print("hours")
main()
