# 💬 PyCAI2

[![Downloads](https://static.pepy.tech/badge/pycai2)](https://pepy.tech/project/pycai2)

An unofficial Python API for Character AI using [curl-cffi](https://github.com/yifeikong/curl_cffi).

 💬 PyCAI1
(https://github.com/kramcat/CharacterAI)

## ❓ Docs & Example

- Docs for PyCAI2: [https://pycai-two.gitbook.io/pycai2/](https://pycai-two.gitbook.io/pycai2/)
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
from PyCAI2 import PyAsyncCAI2

owner_id = '54dbda---------'
char = "piwvxvcMQFwb----------"
room_id = "TiqLm-------------"
voice_target = "E:\\FOLDER\\FOLDER\\FOLDER\\FOLDER\\FOLDER"

clinet = PyAsyncCAI2(owner_id)

async def main():
    message = input("You: ")
     
    # TRANSLATE 
    #TRANSLATE FROM INDONESIA TO ENG
    await clinet.chat2.transl(text=message,target='en',source='id') 

    # GET HISTORIES
    await clinet.chat2.get_histories(char=char)
    
    # GET HISTORY
    await clinet.chat2.get_history(char=char)

    # GET AVATAR
    await clinet.chat2.get_avatar(char=char)

    # CREATE IMAGE
    async with clinet.connect(owner_id) as chat2:
        # RETUR MESSAGE + IMAGE LINK 
        await chat2.create_img(char=char,text=message,
                               author_name='FALCO',
                               Return_all=True)
        # RETURN IMAGE LINK
        await chat2.create_img(char=char,text=message,
                               author_name='FALCO',
                               Return_img=True)
        
    # SEND MESSAGE
    async with clinet.connect(owner_id) as chat2:
        # RETURN W NAME {(CHAR NAME) + MESSAGE}
        await chat2.send_message(char=char,
                                 text=message,
                                 author_name="FALCO",
                                 Return_name=True)
        
        # RETURN WITHOUT NAME (MESSAGE)
        await chat2.send_message(char=char,
                                 text=message,
                                 author_name="FALCO",
                                 Return_name=False)
    
    # NEW CHAT
    async with clinet.connect(owner_id) as chat2:
        # RETURN WITH GREETING
        await chat2.new_chat(char=char,with_greeting=True)

        # RETURN WITHOUT GREETING 
        await chat2.new_chat(char=char,with_greeting=False)

    # DELATE MESSAGE 
    async with clinet.connect(owner_id) as chat2:
        # GET TURN ID FROM HISTORY FUNCTION!
        await chat2.delete_message(char=char, turn_ids=trun_id)
```

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=FalcoTK/PyCAI2&type=Date)](https://star-history.com/#FalcoTK/PyCAI2&Date)
