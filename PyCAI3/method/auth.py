from ..error import AuthError, ServerError
from curl_cffi.requests import Session
import logging


class Authentication:
    """A class for handling user authentication and obtaining a token
    from Character.AI.

    #### Auth By @kramcat (https://github.com/kramcat)"""

    KEY = "AIzaSyAbLy_s6hJqVNr2ZN0UHHiCbJX1X8smTws"
    FIREURL = f"https://identitytoolkit.googleapis.com/v1/accounts"
    URL = "https://beta.character.ai/dj-rest-auth/google_idp/"
    FIREHEADERS = {
        # Firebase key for GoogleAuth API
        "X-Firebase-AppCheck": (
            "eyJraWQiOiJYcEhKU0EiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9."
            "eyJzdWIiOiIxOjQ1ODc5NzcyMDY3NDp3ZWI6YjMzNGNhNDM2MWU5MzRkYWViOWQzYiIsIm"
            "F1ZCI6WyJwcm9qZWN0c1wvNDU4Nzk3NzIwNjc0IiwicHJvamVjdHNcL2NoYXJhY3Rlci1h"
            "aSJdLCJwcm92aWRlciI6InJlY2FwdGNoYV9lbnRlcnByaXNlIiwiaXNzIjoiaHR0cHM6XC"
            "9cL2ZpcmViYXNlYXBwY2hlY2suZ29vZ2xlYXBpcy5jb21cLzQ1ODc5NzcyMDY3NCIsImV4"
            "cCI6MTcxMTAxNzE2MiwiaWF0IjoxNzEwNDEyMzYyLCJqdGkiOiJkSXlkWVFPZEhnaTRmc2"
            "ZGUHMtWHNZVU0zZG01eFY4R05ncDItOWxCQ2xVIn0.o2g6-5Pl7rjiKdQ4X9bdOe6tDSVm"
            "dODFZUljHDnF5cNCik6masItwpeL3Yh6h78sQKNwuKzCUBFjsvDsEIdu71gW4lAuDxhKxl"
            "jffX9nRuh8d0j-ofmwq_4abpA3LdY12gIibvMigf3ncBQiJzu4SVQUKEdO810oUG8G4RWl"
            "QfBIo-PpCO8jhyGZ0sjcklibEObq_4-ynMZnhTuIN_J183-RibxiKMjMTVaCcb1XfPxXi-"
            "zFr2NFVhSM1oTWSYmhseQ219ppHA_-cQQIH6MwC0haHDsAAntjQkjbnG2HhPQrigdbeiXf"
            "pMGHAxLRXXsgaPuEkjYFUPoIfIITgvkj5iJ-33vji2NgmDCpCmpxpx5wTHOC8OEZqSoCyi"
            "3mOkJNXTxOHmxvS-5glMrcgoipVJ3Clr-pes3-aI5Yw7n3kmd4YfsKTadYuE8vyosq_Mpl"
            "EQKolRKj67CSNTsdt2fOsLCWNohduup6qJrUroUpN35R9JuUWgSy7Y4MI6NM-bKJ"
        ),
    }

    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def SendLink(self, email: str) -> bool:
        """
        Sends a link to your email.

        #### Args:
            email (str): your email address.

        #### Returns:
            bool: True if the link is sent successfully.

        #### Raises:
            ServerError: If the link fails to send.
        """
        with Session(impersonate="chrome120") as s:
            response = s.post(
                f"{self.FIREURL}:sendOobCode?key={self.KEY}",
                json={
                    "requestType": "EMAIL_SIGNIN",
                    "email": email,
                    "clientType": "CLIENT_TYPE_WEB",
                    "continueUrl": "https://beta.character.ai",
                    "canHandleCodeInApp": True,
                },
            )

        data = response.json()

        if "email" in data and data["email"] == email:
            return True
        else:
            logging.error(
                f"Failed to send sign-in link: {data.get('error', {}).get('message', 'Unknown error')}"
            )
            raise ServerError(data["error"]["message"])

    def _GetOOBCode(self, link: str) -> str:
        """Extract the oobCode from the sign-in link."""
        with Session(impersonate="chrome120") as s:
            try:
                r = s.get(link, allow_redirects=True)
                return r.url.split("oobCode=")[1].split("&")[0]
            except IndexError:
                logging.error("Invalid link: oobCode not found.")
                raise AuthError("Invalid link: oobCode not found.")

    def _GetFireBaseToken(self, oob_code: str, email: str) -> str:
        """Sign in to Firebase with the oobCode and get the idToken."""
        with Session(impersonate="chrome120") as s:
            response = s.post(
                f"{self.FIREURL}:signInWithEmailLink?key={self.KEY}",
                headers=self.FIREHEADERS,
                json={"email": email, "oobCode": oob_code},
            )

        try:
            id_token = response.json()["idToken"]
            return id_token
        except KeyError:
            logging.error(
                f"Failed to retrieve idToken: {response.json().get('error', {}).get('message', 'Unknown error')}"
            )
            raise AuthError(response.json()["error"]["message"])

    def GetToken(self, link: str, email: str) -> str:
        """
        Get your account token

        #### Args:
            link (str): The sign-in link from your email.
            email (str): Your email address.

        #### Returns:
            str: Token Account

        #### Raises:
            AuthError: If the key cannot be retrieved.
        """
        oob_code = self._GetOOBCode(link)
        id_token = self._GetFireBaseToken(oob_code, email)

        with Session(impersonate="chrome120") as s:
            response = s.post(
                self.URL,
                json={"id_token": id_token},
            )

        try:
            return response.json()["key"]
        except KeyError:
            logging.error(
                f"Failed to retrieve Character.AI key: {response.json().get('error', 'Unknown error')}"
            )
            raise AuthError(response.json()["error"])
