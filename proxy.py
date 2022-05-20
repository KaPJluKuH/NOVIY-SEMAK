import requests
import random
from bs4 import BeautifulSoup as bs
from random import choice


def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # получаем ответ HTTP и создаем объект soup
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", class_='table table-striped table-bordered').find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    # print(proxies)
    return proxies


def main_proxy():
    free_proxies = get_free_proxies()
    my_proxy = choice(free_proxies)
    http_proxy = f"http://{my_proxy}"
    # https_proxy = f"https://{my_proxy}"
    # ftp_proxy = f"ftp://{my_proxy}"
    proxies = {
        "http": http_proxy,
        # "https": https_proxy,
        # "ftp": ftp_proxy
    }
    # print(proxies)
    return proxies
    # print(f'Обнаружено бесплатных прокси - {len(free_proxies)}:')
    # for i in range(len(free_proxies)):
    #     print(f"{i+1}) {free_proxies[i]}")


# def get_session(proxies):
#     # создать HTTP‑сеанс
#     session = requests.Session()
#     # выбираем один случайный прокси
#     proxy = random.choice(proxies)
#     session.proxies = {"http": proxy, "https": proxy}
#     return session
#
#
# for i in range(5):
#     s = get_session(proxies)
#     try:
#         print("Страница запроса с IP:", s.get("http://icanhazip.com", timeout=1.5).text.strip())
#     except Exception as e:
#         continue