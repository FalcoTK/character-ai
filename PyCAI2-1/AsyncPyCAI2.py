from contextlib import asynccontextmanager
from PIL import Image
import io
import websockets
import tls_client as tls
import json
import base64
from pydub import AudioSegment
from io import BytesIO
from typing import Optional
from easygoogletranslate import EasyGoogleTranslate as esgt



# ______         ______ _______ _______ ______ 
# |   __ \ __ __ |      |   _   |_     _|__    |
# |    __/|  |  ||   ---|       |_|   |_|    __|
# |___|   |___  ||______|___|___|_______|______|
#         |_____|                                 

                                                           
# BUILD BY @Falco_TK (https://github.com/FalcoTK)
# CODE  BY @kramcat  (https://github.com/kramcat)
# PATCH BY @kpopdev  (https://github.com/kpopdev)


# PLEASE IF YOU HAVE SOMTING WRONG DM ME IN DISCORD ASAP! (discord: tokaifalco_)                                                  
# ==================================================

__all__ = ['PyCAI2', 'PyAsyncCAI2']


class PyCAI2EX(Exception):
    pass

class ServerError(PyCAI2EX):
    pass

class LabelError(PyCAI2EX):
    pass

class AuthError(PyCAI2EX):
    pass

class PostTypeError(PyCAI2EX):
    pass


class PyAsyncCAI2:
    def __init__(
        self, token: str = None, plus: bool = False
    ):
        self.token = token
        self.plus = plus
        if plus: sub = 'plus'
        else: sub = 'beta'

        self.session = tls.Session(
            client_identifier='okhttp4_android_13'
        )

        setattr(self.session, 'url', f'https://{sub}.character.ai/')
        setattr(self.session, 'token', token)
        
        self.chat = self.chat(token, self.session)
        self.chat2 = self.chat2(token, None, self.session)

    async def request(
        url: str, session: tls.Session,
        *, token: str = None, method: str = 'GET',
        data: dict = None, split: bool = False,
        split2: bool = False, neo: bool = False, 
    ):
        

        if neo:
            link = f'https://neo.character.ai/{url}'
        else:
            link = f'{session.url}{url}'

        if token == None:
            key = session.token
        else:
            key = token

        headers = {
            'User-Agent': 'okhttp/5.0.0-SNAPSHOT',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://beta.character.ai/',
            'Authorization': f'Token {key}',
            'Origin': 'https://beta.character.ai',
        }

        if method == 'GET':
            response = session.get(
                link, headers=headers
            )

        elif method == 'POST':
            response = session.post(
                link, headers=headers, json=data
            )

        elif method == 'PUT':
            response = session.put(
                link, headers=headers, json=data
            )

        if split:
            data = json.loads(response.text.split('\n')[-2])
        elif split2:
            lines = response.text.strip().split('\n')
            data = [json.loads(line) for line in lines if line.strip()] # List
        else:
            data = response.json()

        if str(data).startswith("{'command': 'neo_error'"):
            raise ServerError(data['comment'])
        elif str(data).startswith("{'detail': 'Auth"):
            raise AuthError('Invalid token')
        elif str(data).startswith("{'status': 'Error"):
            raise ServerError(data['status'])
        elif str(data).startswith("{'error'"):
            raise ServerError(data['error'])
        else:
            return data

    async def ping(self):
        return self.session.get(
            'https://neo.character.ai/ping/'
        ).json()

    @asynccontextmanager
    async def connect(self, token: str = None):
        try:
            if token == None: key = self.token
            else: key = token

            setattr(self.session, 'token', key)

            try:
                self.ws = await websockets.connect(
                    'wss://neo.character.ai/ws/',
                     extra_headers = {
                        'Cookie': f'HTTP_AUTHORIZATION="Token {key}"',
                        'origin': 'https://neo.character.ai',
                        'Upgrade': 'websocket',
                        'Sec-WebSocket-Extensions': 'permessage-deflate',
                        'Host': 'neo.character.ai',
                        'User-Agent': 'okhttp/5.0.0-SNAPSHOT',
                    }  
                )
            except websockets.exceptions.InvalidStatusCode:
                raise AuthError('Invalid token')
            
            yield PyAsyncCAI2.chat2(key, self.ws, self.session)
        finally:
            await self.ws.close()  


    class chat:
        def __init__(
            self, token: str, session: tls.Session
        ):
            self.token = token
            self.session = session

        async def room_chat(
            self, characterId: str, voiceId: str, 
            text: str, *, token: str = None,
            **kwargs
        ):
            response = await PyAsyncCAI2.request(
                'chat/streaming/', self.session,
                token=token, method='POST', split2='True',
                data={
                    "character_external_id": characterId,
                    "enable_tti": None,
                    "filter_candidates": None,
                    "give_room_introductions": True,
                    "history_external_id": voiceId,
                    "image_description": "",
                    "image_description_type": "",
                    "image_origin_type": "",
                    "image_rel_path": "",
                    "initial_timeout": None,
                    "insert_beginning": None,
                    "is_proactive": False,
                    "mock_response": False,
                    "model_properties_version_keys": "",
                    "model_server_address": None,
                    "model_server_address_exp_chars": None,
                    "num_candidates": 1,
                    "override_prefix": None,
                    "override_rank": None,
                    "parent_msg_uuid": None,
                    "prefix_limit": None,
                    "prefix_token_limit": None,
                    "rank_candidates": None,
                    "ranking_method": "random",
                    "retry_last_user_msg_uuid": None,
                    "rooms_prefix_method": "",
                    "seen_msg_uuids": [],
                    "staging": False,
                    "stream_every_n_steps": 16,
                    "stream_params": None,
                    "text": text,
                    "tgt": None,
                    "traffic_source": None,
                    "unsanitized_characters": None,
                    "voice_enabled": True,
                    **kwargs
                }
            )

            merged_audio = AudioSegment.silent(duration=0)

            for i, json_parsed in enumerate(response):
                replies = json_parsed.get("replies", [])

                for reply in replies:
                    text = reply.get("text", "")

                encode = json_parsed.get("speech", "")
                if encode:
                    decode = base64.b64decode(encode)
                    audio = AudioSegment.from_file(BytesIO(decode))
                    merged_audio += audio
                else:
                    print(f"Skipping .json #{i}") # Intentionally skips due to how c.ai api works

            # Exporting the merged audio to voice.mp3
            merged_audio.export("voice.mp3", format="mp3")

            return {"text": text, "voice": "voice.mp3"}

        async def next_message(
            self, history_id: str, parent_msg_uuid: str,
            tgt: str, *, token: str = None, **kwargs
        ):
            response = await PyAsyncCAI2.request(
                'chat/streaming/', self.session,
                token=token, method='POST', split=True,
                data={
                    'history_external_id': history_id,
                    'parent_msg_uuid': parent_msg_uuid,
                    'tgt': tgt,
                    **kwargs
                }
            )

        async def get_histories(
            self, char: str, *, number: int = 50,
            token: str = None
        ):
            return await PyAsyncCAI2.request(
                'chat/character/histories_v2/', self.session,
                token=token, method='POST',
                data={'external_id': char, 'number': number},
            )

        async def get_history(
            self, history_id: str = None,
            *, token: str = None
        ):
            return await PyAsyncCAI2.request(
                'chat/history/msgs/user/?'
                f'history_external_id={history_id}',
                self.session, token=token
            )

        async def get_chat(
            self, char: str = None, *,
            token: str = None
        ):
            return await PyAsyncCAI2.request(
                'chat/history/continue/', self.session,
                token=token, method='POST',
                data={
                    'character_external_id': char
                }
            )

        async def send_message(
            self, history_id: str, tgt: str, text: str,
            *, token: str = None, **kwargs
        ):
            
            return await PyAsyncCAI2.request(
                'chat/streaming/', self.session,
                token=token, method='POST', split=True,
                data={
                    'history_external_id': history_id,
                    'tgt': tgt,
                    'text': text,
                    **kwargs
                }
            )

        async def delete_message(
            self, history_id: str, uuids_to_delete: list,
            *, token: str = None, **kwargs
        ):
            return await PyAsyncCAI2.request(
                'chat/history/msgs/delete/', self.session,
                token=token, method='POST',
                data={
                    'history_id': history_id,
                    'uuids_to_delete': uuids_to_delete,
                    **kwargs
                }
            )

        async def new_chat(
            self, char: str, *, token: str = None
        ):
            return await PyAsyncCAI2.request(
                'chat/history/create/', self.session,
                token=token, method='POST',
                data={
                    'character_external_id': char
                }
            )

    class chat2:
        """Managing a chat2 with a character

        chat.next_message('CHAR', 'CHAT_ID', 'PARENT_ID')
        chat.send_message('CHAR', 'CHAT_ID', 'TEXT', {AUTHOR})
        chat.next_message('CHAR', 'MESSAGE')
        chat.new_chat('CHAR', 'CHAT_ID', 'CREATOR_ID')
        chat.get_histories('CHAR')
        chat.get_chat('CHAR')
        chat.get_history('CHAT_ID')
        chat.rate(RATE, 'CHAT_ID', 'TURN_ID', 'CANDIDATE_ID')
        chat.delete_message('CHAT_ID', 'TURN_ID')

        """
        def __init__(
            self, token: str,
            ws: websockets.WebSocketClientProtocol,
            session: tls.Session
        ):
            self.token = token
            self.session = session
            self.ws = ws

        async def transl(text:str, target:str, source:str):
            translator = esgt(
            source_language=source,
            target_language=target)

            resoult = translator.translate(text)

            return resoult

        async def next_message(
            self, char: str, chat_id: str,
            parent_msg_uuid: str
        ):
            await self.ws.send(json.dumps({
                'command': 'generate_turn_candidate',
                'payload': {
                    'character_id': char,
                    'turn_key': {
                        'turn_id': parent_msg_uuid,
                        'chat_id': chat_id
                    }
                }
            }))

            while True:
                response = json.loads(await self.ws.recv())
                try: response['turn']
                except: raise ServerError(response['comment'])
                
                if not response['turn']['author']['author_id'].isdigit():
                    try: is_final = response['turn']['candidates'][0]['is_final']
                    except: pass
                    else: return response

        async def create_img(
            self, char: str, chat_id: str, text: str,
            author: dict = None, Return_img: bool = True, 
            Return_all: bool = False, *, turn_id: str = None,
            custom_id: str = None, candidate_id: str = None
        ):
            if custom_id != None:
                turn_key = {
                    'turn_id': custom_id,
                    'chat_id': chat_id
                }
            else:
                turn_key = {'chat_id': chat_id}
            
            if turn_id != None and candidate_id != None:
                message['update_primary_candidate'] = {
                    'candidate_id': candidate_id,
                    'turn_key': {
                        'turn_id': turn_id,
                        'chat_id': chat_id
                    }
                }

            message = {
                'command': 'create_and_generate_turn',
                'payload': {
                    'character_id': char,
                    'turn': {
                        'turn_key': turn_key,
                        'author': author,
                        'candidates': [{'raw_content': text}]
                    }
                }
            }

            await self.ws.send(json.dumps(message))
            
            while True:
                response = json.loads(await self.ws.recv())
                try: response['turn']
                except: raise ServerError(response['comment'])
                
                if not response['turn']['author']['author_id'].isdigit():
                    try: is_final = response['turn']['candidates'][0]['is_final']
                    except: pass
                    else:
                        if Return_all:
                            r_in = response['turn']['candidates'][0]['raw_content']
                            img_in = response['turn']['candidates'][0]['tti_image_rel_path']  # Perhatikan perubahan indeks ke 0 di sini
                            results = f"{r_in}\n{img_in}"
                            return results
                        if Return_img:
                            r = response['turn']['candidates'][0]['tti_image_rel_path']
                            return r

        async def send_message(
            self, char: str, chat_id: str,
            text: str, author: dict = None,
            *, turn_id: str = None, custom_id: str = None,
            candidate_id: str = None, Return_name: bool = False
        ):  

            if custom_id != None:
                turn_key = {
                    'turn_id': custom_id,
                    'chat_id': chat_id
                }
            else:
                turn_key = {'chat_id': chat_id}
            
            message = {
                'command': 'create_and_generate_turn',
                'payload': {
                    'character_id': char,
                    'turn': {
                        'turn_key': turn_key,
                        'author': author,
                        'candidates': [{'raw_content': text}]
                    }
                }
            }

            if turn_id != None and candidate_id != None:
                message['update_primary_candidate'] = {
                    'candidate_id': candidate_id,
                    'turn_key': {
                        'turn_id': turn_id,
                        'chat_id': chat_id
                    }
                }
        
            await self.ws.send(json.dumps(message))

            while True:
                response = json.loads(await self.ws.recv())
                try: response['turn']
                except: raise ServerError(response['comment'])
                
                if not response['turn']['author']['author_id'].isdigit():
                    try: is_final = response['turn']['candidates'][0]['is_final']
                    except: pass
                    else:
                        if Return_name:
                            r_in = response['turn']['candidates'][0]['raw_content']
                            n_in = response['turn']['author']["name"]
                            r = f"({n_in}) {r_in}"
                            return r
                        else:
                            r = response['turn']['candidates'][0]['raw_content']
                            return r
        

        async def new_chat(
            self, char: str, chat_id: str,
            creator_id: str, *, with_greeting: bool = True
        ):
            message = {
                'command': 'create_chat',
                'payload': {
                    'chat': {
                        'chat_id': chat_id,
                        'creator_id': creator_id,
                        'visibility': 'VISIBILITY_PRIVATE',
                        'character_id': char,
                        'type': 'TYPE_ONE_ON_ONE'
                    },
                    'with_greeting': with_greeting
                }
            }
            await self.ws.send(json.dumps(message))

            response = json.loads(await self.ws.recv())
            
            try: response['chat']
            except KeyError:
                raise ServerError(response['comment'])
            else:
                answer = json.loads(await self.ws.recv())
                return response, answer
        

        async def get_histories(
            self, char: str = None, *,
            preview: int = 2, token: str = None
        ):
            return await PyAsyncCAI2.request(
                f'chats/?character_ids={char}'
                f'&num_preview_turns={preview}',
                self.session, token=token, neo=True
            )


        async def get_history(
            self, chat_id: str = None, *,
            token: str = None
        ):
            return await PyAsyncCAI2.request(
                f'turns/{chat_id}/', self.session,
                token=token, neo=True
            )


        async def delete_message(
            self, chat_id: str, turn_ids: list,
            *, token: str = None, **kwargs
        ):
            payload = {
                'command':'remove_turns',
                'payload': {
                    'chat_id': chat_id,
                    'turn_ids': turn_ids
                }
            }

            await self.ws.send(json.dumps(payload))
            return json.loads(await self.ws.recv())
        
