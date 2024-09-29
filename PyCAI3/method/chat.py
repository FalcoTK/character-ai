from ..error import ServerError, AuthError, NotFoundError
import websockets
from websockets import exceptions
import asyncio
import logging
import json


class Chat:
    def __init__(self, token: str = None):
        """
        Initialize the Chat class.

        :param token: The authorization token for the WebSocket connection.
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.ws = None
        self.token = token
        self.uri = "wss://neo.character.ai/ws/"

    async def connect(self):
        """Establish the WebSocket connection."""
        if self.ws is None:  # Only connect if not already connected
            self.ws = await self.__connect()

    async def sendMessage(
        self,
        charID: str,
        message: str,
        chatID: str,
        customTurn: str = None,
        author: dict = {},
    ):
        """Send a message to the WebSocket server."""
        await self.connect()

        TurnKey = {"chat_id": chatID}
        if customTurn is not None:
            TurnKey["turn_id"] = customTurn

        payload = {
            "command": "create_and_generate_turn",
            "payload": {
                "tts_enabled": True,
                "character_id": charID,
                "user_name": "FxC4",
                "turn": {
                    "turn_key": {
                        "turn_id": "",
                        "chat_id": chatID,
                    },
                    "candidates": [
                        {
                            "raw_content": message,
                        }
                    ],
                },
            },
        }

        await self.ws.send(json.dumps(payload))

        try:
            while True:
                response = await self.ws.recv()
                ParasedResponse = json.loads(response)
                if "turn" in ParasedResponse:
                    turn = ParasedResponse["turn"]
                    if not turn["author"]["author_id"].isdigit():
                        if turn["candidates"][0].get("is_final", False):
                            await self.__close()
                            return turn["candidates"][0]["raw_content"]

        except asyncio.TimeoutError:
            self.logger.error("Timeout waiting for a response from the server.")
            await self.__close()
            raise ServerError("Timeout waiting for a response from the server")
        except Exception as e:
            self.logger.error(f"Error in sendMessage: {e}")
            await self.__close()
            raise NotFoundError("Error in sendMessage:", e)

    async def __connect(self) -> websockets.WebSocketClientProtocol:
        """
        Establishes a WebSocket connection to the Character.ai platform.
        """
        try:
            if self.token is None:
                raise AuthError("Did you add token?")

            self.logger.info("Attempting to connect to WebSocket...")

            self.ws = await websockets.connect(
                self.uri,
                extra_headers={
                    "Authorization": f"Token {self.token}",
                },
                timeout=10,
            )

            self.logger.info("WebSocket connection established successfully.")
            return self.ws

        except exceptions.InvalidStatusCode as err:
            self.logger.error(f"WebSocket connection failed with error: {err}")
            raise ServerError(f"WebSocket connection failed with error: {err}")

        except Exception as e:
            self.logger.error(f"Unexpected error during connection: {e}")
            raise

    async def __close(self):
        """Close the WebSocket connection."""
        if self.ws is not None:
            await self.ws.close()
            self.ws = None
            self.logger.info("WebSocket connection closed.")
