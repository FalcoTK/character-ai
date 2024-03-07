# 💬 PyCAI2
[![Downloads](https://static.pepy.tech/badge/pycai2)](https://pepy.tech/project/pycai2)

An unofficial API for Character AI for Python using [tls-client](https://github.com/FlorianREGAZ/Python-Tls-Client)
and this is a new version of PyCAI

 💬 PyCAI1
this is the frist version 
(https://github.com/kpopdev/CharacterAI)

# ❓ DOCS
click to go docs of PyCAI2 
[![DOCS](https://tokais-creator.gitbook.io/pycai2/)

# 🏅 My Comunity
**THIS IS VERSION 2.0.2 UNDER DEVLOP PLEASE JOIN THE SERVER FOR NEW UPDATE!**
[**https://discord.gg/xxaA8eKMvM**](https://discord.gg/xxaA8eKMvM)


## 💻 Installation
```bash
pip install PyCAI2
```
🔑 Get Token 
DO NOT SHARE IT
The token is needed for authorization and operation of requests from your account
1. Open DevTools in your browser
2. Go to Storage -> Local Storage -> char_token
3. Copy `value`


📬 Get Char ID
1. Open char with chat2
2. like this:```https://beta.character.ai/chat2?char=piwvxvcMQFwbQXCQpJdzbqPMg9ck4FaYi4NWM86ERXo&source=recent-chats```
3. coppy from char= till &source=
4. like this:
5. ```piwvxvcMQFwbQXCQpJdzbqPMg9ck4FaYi4NWM86ERXo```

👻 Get Chat ID
1. Go to: ```neo.character.ai/chats/recent/ <CHAR ID>```
2. For Exsample: ```neo.character.ai/chats/recent/piwvxvcMQFwbQXCQpJdzbqPMg9ck4FaYi4NWM86ERXo```
3. Result: ```{"chats": [{"chat_id": "8880583d-fa2c-47f8-89e6-4fcf09c14a38",```
4. Coppy the chat id

🕵️ Get Chat Author
1. Same Website Like get chat id
2. Result: ``` 117205Z", "creator_id": "474480773", "character_id":```
3. coppy the creator id 
 

## 📙 Example
```Python
from charaiPY.AsyncPyCAI2 import PyAsyncCAI2 #IMPORT THE LIB
import tls_client as tls #IMPORT LIB
import asyncio as ass #IMPORT LIB

owner_id = 'TOKEN!' #TOKEN 
char = "CHAR ID!" #CHAR ID
chat_id = "CHAT ID!" #CHAT ID

aut_set ={
    "author_id": "<CREATOR ID>", #CREATOR ID
    "is_human": True, #PLEASE DONT WRITE TO FALSE
    "name": "<WRITE YOUR C.AI NAME>" #YOUR CAI NAME 
}

client = PyAsyncCAI2(owner_id) #inport owner id

async def main():
    message = input("You:") #input text
#how this work?
#i use websockets ti get connectio
    async with client.connect(owner_id) as chat2: #Make connection to server
        r = await chat2.send_message(char,
                 chat_id, message, aut_set,
                 Return_name=True) #ALL VARIABLE WILL SENT TO SERVER
#IF YOU WANT TO THE OUTPUT WHITHOUT NAME YOH CAN DO RETURN_NAME=FALSE
        print(r)

while True:
    ass.run(main())
```

