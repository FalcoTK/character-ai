import logging
import logging.config
from curl_cffi.requests import Session

from typing import Any, Dict, List, Type

from ..erorr import AuthError, ServerError, JSONError, NotFoundError
from curl_cffi.requests import Session, CurlMime
import json
import websockets
from websockets import exceptions
import asyncio


class Request:
    def __init__(self, session: Session):
        self.session = session
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

    async def request(
        self,
        url: str,
        *,
        token: str = None,
        method: str = "GET",
        data: dict = None,
        split: bool = False,
        neo: bool = False,
        multipart: CurlMime = None,
    ):
        key = self.token or token
        if not key:
            raise AuthError("No token")

        headers = {"Authorization": f"Token {key}"}
        link = f"https://plus.character.ai/{url}"

        if neo:
            link = link.replace("plus", "neo")

        data = data or {}

        session = Session()  # Create a session using curl_cffi

        try:
            if multipart:  # Handling multipart requests
                r = session.post(link, headers=headers, data=data, mime=multipart)
            elif method == "POST":
                r = session.post(link, headers=headers, json=data)
            elif method == "PUT":
                r = session.put(link, headers=headers, json=data)
            elif method == "GET":
                r = session.get(link, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            # Check for errors in neo responses
            if neo and not r.ok:
                try:
                    raise ServerError(r.json().get("comment", r.text))
                except KeyError:
                    raise ServerError(r.text)

            if r.status_code == 404:
                raise ServerError("Not Found")
            elif not r.ok:
                raise ServerError(f"Server returned status code: {r.status_code}")
            # Handle JSON response parsing
            text = r.text
            if "}\n{" in text and split:
                text = "{" + text.split("}\n{")[-1]

            try:
                res = json.loads(text)
            except json.JSONDecodeError:
                raise JSONError(f"Unable to decode JSON. Server response: {r.text}")

            if res.get("force_login"):
                raise AuthError("I need Auth >:C")
            if res.get("status") != "OK" or res.get("abort"):
                raise ServerError(res.get("error", "Unknown error"))
            if res.get("error"):
                raise ServerError(res["error"])

            return res

        except Exception as e:
            raise ServerError(f"Request failed: {e}")

        finally:
            session.close()


class Wss:
    def __init__(self, token: str = None):
        """
        Initialize the WSConnect class for establishing a WebSocket connection.

        :param token: The user's authentication token. If not provided, it will be set to None.
        """
        self.token = token
        logging.basicConfig(
            level=logging.INFO
        )  # Changed log level to INFO for more detailed logs
        self.logger = logging.getLogger(__name__)
        self.ws_url = "wss://neo.character.ai/ws/"
        self.headers = {
            "Authorization": f"Token {self.token}",
        }
        self.ws = None

    async def __connect(self) -> websockets.WebSocketClientProtocol:
        """
        Establishes a WebSocket connection to the Character.ai platform.

        :return: A WebSocketClientProtocol object representing the established connection.

        :raises: ServerError: If the WebSocket connection fails due to an InvalidStatusCode error.
        """
        try:
            try:
                self.logger.info(
                    "Attempting to connect to WebSocket..."
                )  # Added logging
                self.ws = await websockets.connect(
                    self.ws_url, extra_headers=self.headers
                )
                self.logger.info("WebSocket connection established successfully.")
                return self.ws  # Explicitly returning WebSocket connection object
            except exceptions.InvalidStatusCode as err:
                self.logger.error(f"WebSocket connection failed with error: {err}")
                raise ServerError("WebSocket connection failed with error: " + str(err))
        finally:
            if self.ws is not None:
                await self.ws.close()
                self.logger.info(
                    "WebSocket connection closed."
                )  # Added logging for closure

    async def send(self, message: str):
        """
        Send a message through the established WebSocket connection.
        """
        if self.ws is None:
            raise ConnectionError("WebSocket connection not established.")

        self.logger.info(f"Sending message: {message}")
        await self.ws.send(message)

    async def receive(self):
        """
        Receive a message from the established WebSocket connection.
        """
        if self.ws is None:
            raise ConnectionError("WebSocket connection not established.")

        message = await self.ws.recv()
        self.logger.info(f"Received message: {message}")
        return message


# class WSS:
#     """
#     WSConnect class manages the WebSocket connection to the Character.ai platform.

#     Initialize the WSConnect class for establishing a WebSocket connection.

#         :param token: The user's authentication token. If not provided, it will be set to None.
#         :param start: Indicates whether to immediately start the WebSocket connection. Default is True.
#         :param Dev: Enables developer mode for additional logging. Default is False.

#     Features:
#     - Establishes and manages WebSocket connections.
#     - Supports custom token-based authentication.
#     - Includes developer mode for enhanced logging.
#     """

#     def __init__(self, token: str = None, start: bool = True, dev: bool = False):
#         self.token = token
#         self.ws_url = "wss://neo.character.ai/ws/"
#         self.headers = {
#             "Authorization": f"Token {self.token}",
#         }
#         self.websocket = None

#         # Configure logging
#         logging.basicConfig(level=logging.INFO if dev else logging.WARNING)
#         self.logger = logging.getLogger(__name__)

#         if start:
#             asyncio.run(self.ConnectWS())

#     async def ConnectWS(self):
#         """Establish the WebSocket connection."""
#         try:
#             self.websocket = await websockets.connect(
#                 self.ws_url, extra_headers=self.headers
#             )
#             self.logger.info("Connected to WebSocket")
#             asyncio.create_task(self.handle_messages())
#         except Exception as e:
#             self.logger.error(f"Error when trying to connect to WebSocket: {e}")
#             raise ServerError("Error when trying to connect to WebSocket")

#     async def DumpWS(self, data: dict):
#         """Send data to the WebSocket."""
#         try:
#             if not self.websocket:
#                 raise ServerError("Cannot connect to WebSocket")
#             await self.websocket.send(json.dumps(data))
#             self.logger.info(f"Sent data to WebSocket: {data}")
#         except Exception as e:
#             self.logger.error(f"Error when sending JSON to WebSocket: {e}")
#             raise ServerError("Error when sending JSON to WebSocket")

#     async def RecvWS(self):
#         """Receive data from the WebSocket."""
#         while self.websocket:
#             try:
#                 message = await self.websocket.recv()  # Receive message from server
#                 response = json.loads(message)  # Parse the JSON response
#                 self.logger.info(f"Received payload: {response}")
#                 return response
#             except websockets.ConnectionClosed as e:
#                 self.logger.warning(f"WebSocket connection closed: {e}")
#                 break
#             except Exception as e:
#                 self.logger.error(f"Error while receiving message: {e}")
#                 raise NotFoundError(f"Error: {e}")
#         return None  # Explicitly return None if no message is received

#     async def CloseWS(self):
#         """Close the WebSocket connection."""
#         if self.websocket:
#             await self.websocket.close()
#             self.logger.info("WebSocket connection closed")


def flatten(a: Dict[str, Any], ParameterKey: str = "", sep: str = "") -> Dict[str, Any]:
    """
    Flattens a nested dictionary structure into a single-level dictionary.

    :param a: Dictionary to be flattened.
    :param ParameterKey: Optional prefix for nested keys (used in recursion).
    :param sep: Separator used between nested key names.
    :return: A flattened dictionary.
    """
    if not isinstance(a, dict):
        raise ValueError("Expected a dictionary as input.")

    items = []
    for k, v in a.items():
        if v == "":
            v = None  # Convert empty strings to None (if needed)

        # Build the key string
        new_key = f"{ParameterKey}{sep}{k}" if ParameterKey else k

        if isinstance(v, dict):
            # Recursive call for nested dictionaries
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))  # Add flattened key-value pair

    return dict(items)


def Validate(_class: Type[Any], data: List[Dict[str, Any]]) -> List[Any]:
    """
    Validates and transforms a list of dictionaries into a list of instances of a given class.

    :param _class: The class to instantiate with the dictionary data.
    :param data: List of dictionaries, each representing the attributes of the class.
    :return: A list of instances of the given class.
    :raises: ValueError if the data is not a list of dictionaries or if instantiation fails.
    """
    if not isinstance(data, list):
        raise ValueError("Data should be a list of dictionaries.")

    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each item in the data list should be a dictionary.")

    try:
        return [_class(**a) for a in data]
    except TypeError as e:
        raise ValueError(f"Error instantiating {_class}: {e}")
