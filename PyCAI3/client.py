import logging
from curl_cffi.requests import Session
from .method.ReqHandeler import RH

PYcai3 = """
 _____     _____ _____ _____    _____ ___ 
|  _  |_ _|     |  _  |     |  |  |  |_  |
|   __| | |   --|     |-   -|  |  |  |_  |
|__|  |_  |_____|__|__|_____|   \___/|___|
      |___|                               
      
      Discord: https://discord.gg/DCjeH7pEGa
      Github: https://github.com/FalcoTK
"""


class PyCAI3:
    def __init__(
        self, token: str = None, plus: bool = False, Dev: bool = False
    ) -> None:
        """
        Initialize PyCAI3 class with token, plus, and Dev parameters.

        :param token (str): The API token for authentication. Default is None.
        :param plus (bool): A flag indicating whether to enable additional features. Default is False.
        :param Dev (bool): A flag indicating whether to enable development mode. Default is False.

        In development mode, logging is set up with INFO level.

        The session object is initialized with a custom User-Agent header and the base URL is set.
        The token is also assigned to the session object.
        -----

        get some help:

        Discord: https://discord.gg/DCjeH7pEGa

        Github: https://github.com/FalcoTK
        """
        self.token = token
        self.plus = plus
        self.Dev = Dev

        if self.Dev:
            logging.basicConfig(level=logging.INFO)
            logging.info(PYcai3)

        self.session = Session(headers={"User-Agent": "okhttp/5.0.0-SNAPSHOT"})
        setattr(self.session, "url", "https://character.ai/")
        setattr(self.session, "token", token)

    async def ping(self):
        if self.Dev:
            logging.info("Pinging server...")

        handler = RH(session=self.session, Dev=self.Dev)
        if self.Dev:
            return await handler.RequstGET(url="ping", neo=True)

        # Without DevMode
        rtnRequst = await handler.RequstGET(url="ping", neo=True)
        return rtnRequst["status"]
