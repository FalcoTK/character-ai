# 💬 PyCAI2
![Tag](https://img.shields.io/github/license/kramcat/CharacterAI)

An unofficial API for Character AI for Python using [tls-client](https://github.com/FlorianREGAZ/Python-Tls-Client)
and this is a new version of PyCAI

# 💬 PyCAI1
this is the frist version 
![Tag](https://github.com/kpopdev/CharacterAI)

# 🏅 My Comunity
**THIS IS VERSION 2.0.2 UNDER DEVLOP PLEASE JOIN THE SERVER FOR NEW UPDATE!**
[**https://discord.gg/xxaA8eKMvM**](https://discord.gg/xxaA8eKMvM)


## 💻 Installation
```bash
pip install PyCAI2
```
## 🔑 Get Token 
DO NOT SHARE IT
The token is needed for authorization and operation of requests from your account
1. Open DevTools in your browser
2. Go to Storage -> Local Storage -> char_token
3. Copy `value`


## 📬 Get Char ID
1. Open char with chat2
2. like this:```https://beta.character.ai/chat2?char=piwvxvcMQFwbQXCQpJdzbqPMg9ck4FaYi4NWM86ERXo&source=recent-chats```
3. coppy from char= till &source=
4. like this:
5. ```piwvxvcMQFwbQXCQpJdzbqPMg9ck4FaYi4NWM86ERXo```

## 👻 Get Chat ID
1. Go to: ```neo.character.ai/chats/recent/ <CHAR ID>```
2. For Exsample: ```neo.character.ai/chats/recent/piwvxvcMQFwbQXCQpJdzbqPMg9ck4FaYi4NWM86ERXo```
3. Result: ```{"chats": [{"chat_id": "8880583d-fa2c-47f8-89e6-4fcf09c14a38",```
4. Coppy the chat id
 

## 📙 Example
```Python
from charaiPY.AsyncPyCAI2 import PyAsyncCAI2
import tls_client as tls
import asyncio as ass

owner_id = 'TOKEN!'
char = "CHAR ID!"
chat_id = "CHAT ID!"

aut_set ={
    "author_id": "474480773",
    "is_human": True,
    "name": "Falco"
}

client = PyAsyncCAI2(owner_id)

async def main():
    message = input("You:")
    async with client.connect(owner_id) as chat2:
        r = await chat2.send_message(char, chat_id, message, aut_set, Return_name=True)
        print(r)

while True:
    ass.run(main())
```

