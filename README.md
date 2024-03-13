# 💬 PyCAI2

[![Downloads](https://static.pepy.tech/badge/pycai2)](https://pepy.tech/project/pycai2)

An unofficial Python API for Character AI using [curl-cffi](https://github.com/yifeikong/curl_cffi).

 💬 PyCAI1
(https://github.com/kramcat/CharacterAI)

## ❓ Docs & Example

- Docs for PyCAI2: [https://tokais-creator.gitbook.io/pycai2](https://tokais-creator.gitbook.io/pycai2)
- Discord bot with PyCAI2: [https://github.com/FalcoTK/PyCAI2-Discord](https://github.com/FalcoTK/PyCAI2-Discord)

## 🏅 Community
**THIS IS VERSION 2.0.5 UNDER DEVELOPMENT. PLEASE JOIN THE SERVER FOR NEW UPDATES!
[https://discord.gg/xxaA8eKMvM](https://discord.gg/xxaA8eKMvM)**

## 💻 Installation
```bash
pip install PyCAI2
```
- Donwload FFMPG : https://www.ffmpeg.org/download.html
- guide to install FFMPG: https://youtu.be/IECI72XEox0?si=FFJXulNUZI0AM82y

### 🔑 Get Token 
- **DO NOT SHARE IT**
- The token is needed for authorization and operation of requests from your account.
1. Open DevTools in your browser.
2. Go to Storage -> Local Storage -> `char_token`.
3. Copy the `value`.

### 📬 Get Char ID
1. Open 'char' with 'chat2'.
2. Example URL: `https://beta.character.ai/chat2?char=piwvxvcMQFwbQXCQpJdzbqPMg9ck4FaYi4NWM86ERXo&source=recent-chats`.
3. Copy from `char=` till `&source=`.
4. Example: `piwvxvcMQFwbQXCQpJdzbqPMg9ck4FaYi4NWM86ERXo`.

### 👻 Get Chat ID
1. Go to: `neo.character.ai/chats/recent/ <CHAR ID>`.
2. Example URL: `neo.character.ai/chats/recent/piwvxvcMQFwbQXCQpJdzbqPMg9ck4FaYi4NWM86ERXo`.
3. Result: `{"chats": [{"chat_id": "8880583d-fa2c-47f8-89e6-4fcf09c14a38",`.
4. Copy the chat ID.

### 🕵️ Get Chat Author
1. Same steps as getting Chat ID, instead, get Chat Author.
2. Result: `117205Z", "creator_id": "474480773", "character_id":`.
3. Copy the creator ID.

## 📙 Example
```python
from charaiPY.AsyncPyCAI2 import PyAsyncCAI2 # IMPORT THE LIB
import tls_client as tls # IMPORT LIB
import asyncio as ass # IMPORT LIB

owner_id = 'TOKEN!' # TOKEN 
char = "CHAR ID!" # CHAR ID
chat_id = "CHAT ID!" # CHAT ID

aut_set ={
    "author_id": "<CREATOR ID>", # CREATOR ID
    "is_human": True, # PLEASE DON'T WRITE TO FALSE
    "name": "<WRITE YOUR C.AI NAME>" # YOUR CAI NAME 
}

client = PyAsyncCAI2(owner_id) # IMPORT OWNER ID

async def main():
    message = input("You:") # INPUT TEXT
    # How this works?
    # I use websockets to get connection
    async with client.connect(owner_id) as chat2: # Make a connection to the server
        r = await chat2.send_message(char,
                 chat_id, message, aut_set,
                 Return_name=True) # ALL VARIABLES WILL BE SENT TO SERVER
        # IF YOU WANT THE OUTPUT WITHOUT NAME, YOU CAN SET RETURN_NAME=False
        print(r)

while True:
    ass.run(main())
```

