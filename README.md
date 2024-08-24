Here’s an improved version of the README, with the announcement included and without the star history section:

---

# 💬 PyCAI2

[![Downloads](https://static.pepy.tech/badge/pycai2)](https://pepy.tech/project/pycai2)

An unofficial Python API for Character AI using [curl-cffi](https://github.com/yifeikong/curl_cffi).

**⚠️ ANNOUNCEMENT:**  
This project is scheduled to be discontinued. However, a new and improved version, `PyCAI3`, will be released soon in a different repository. Stay tuned for updates here: [PyCAI3 Repository](https://github.com/FalcoTK/PyCAI3).

## ❓ Documentation & Examples

- [PyCAI2 Documentation](https://pycai-two.gitbook.io/pycai2/)
- [PyCAI2 Discord Bot Example](https://github.com/FalcoTK/PyCAI2-Discord)

## 🏅 Community

Join our Discord server for updates and support: [https://discord.gg/xxaA8eKMvM](https://discord.gg/xxaA8eKMvM).

## 💻 Installation

```bash
pip install PyCAI2
```

1. Download FFmpeg: [https://www.ffmpeg.org/download.html](https://www.ffmpeg.org/download.html)
2. Follow the installation guide: [FFmpeg Installation Guide](https://youtu.be/IECI72XEox0?si=FFJXulNUZI0AM82y)

## 🔑 How to Get Your Token

**Do not share your token.** The token is needed for authorization and operation of requests from your account.

1. Open DevTools in your browser.
2. Go to Storage -> Local Storage -> `char_token`.
3. Copy the `value`.

## 📬 How to Get Character ID

1. Open a character chat in `chat2`.
2. Example URL: `https://beta.character.ai/chat2?char=piwvxvcMQFwbQXCQpJdzbqPMg9ck4FaYi4NWM86ERXo&source=recent-chats`.
3. Copy from `char=` until `&source=`.
4. Example: `piwvxvcMQFwbQXCQpJdzbqPMg9ck4FaYi4NWM86ERXo`.

## 👻 How to Get Chat ID

1. Go to: `neo.character.ai/chats/recent/<CHAR ID>`.
2. Example URL: `neo.character.ai/chats/recent/piwvxvcMQFwbQXCQpJdzbqPMg9ck4FaYi4NWM86ERXo`.
3. Look for the following JSON key: `{"chats": [{"chat_id": "8880583d-fa2c-47f8-89e6-4fcf09c14a38",`.
4. Copy the `chat_id`.

## 🕵️ How to Get Chat Author ID

1. Follow the steps to get the Chat ID.
2. Look for the following JSON key: `"creator_id": "474480773"`.
3. Copy the `creator_id`.

## 📙 Usage Example

```python
from PyCAI2 import PyAsyncCAI2

owner_id = '54dbda---------'
char = "piwvxvcMQFwb----------"
room_id = "TiqLm-------------"
voice_target = "E:\\FOLDER\\FOLDER\\FOLDER\\FOLDER\\FOLDER"

client = PyAsyncCAI2(owner_id)

async def main():
    message = input("You: ")

    # TRANSLATE FROM INDONESIAN TO ENGLISH
    await client.chat2.transl(text=message, target='en', source='id')

    # GET HISTORIES
    await client.chat2.get_histories(char=char)

    # GET HISTORY
    await client.chat2.get_history(char=char)

    # GET AVATAR
    await client.chat2.get_avatar(char=char)

    # CREATE IMAGE
    async with client.connect(owner_id) as chat2:
        # RETURN MESSAGE + IMAGE LINK
        await chat2.create_img(char=char, text=message, author_name='FALCO', Return_all=True)
        # RETURN IMAGE LINK ONLY
        await chat2.create_img(char=char, text=message, author_name='FALCO', Return_img=True)

    # SEND MESSAGE
    async with client.connect(owner_id) as chat2:
        # RETURN MESSAGE WITH NAME
        await chat2.send_message(char=char, text=message, author_name="FALCO", Return_name=True)
        # RETURN MESSAGE WITHOUT NAME
        await chat2.send_message(char=char, text=message, author_name="FALCO", Return_name=False)

    # START A NEW CHAT
    async with client.connect(owner_id) as chat2:
        # WITH GREETING
        await chat2.new_chat(char=char, with_greeting=True)
        # WITHOUT GREETING
        await chat2.new_chat(char=char, with_greeting=False)

    # DELETE MESSAGE
    async with client.connect(owner_id) as chat2:
        # GET TURN ID FROM HISTORY FUNCTION
        await chat2.delete_message(char=char, turn_ids=turn_id)
```
