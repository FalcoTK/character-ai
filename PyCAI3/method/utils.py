import logging
import logging.config
from curl_cffi.requests import Session

from typing import Any, Dict, List, Type

from ..error import AuthError, ServerError, JSONError, NotFoundError
from curl_cffi.requests import Session, CurlMime
import json


class Request:
    def __init__(self, session: Session, logging_level: int = logging.INFO):
        self.session = session
        self.token = None  # Ensure token is initialized if not passed in request
        logging.basicConfig(level=logging_level)
        self.logger = logging.getLogger(__name__)

    async def request(
        self,
        url: str,
        *,
        token: str = None,
        method: str = "GET",
        data: Dict[str, Any] = None,
        split: bool = False,
        neo: bool = False,
        multipart: CurlMime = None,
    ):
        # Ensure we have a token
        key = self.token or token
        if not key:
            self.logger.error("No token provided for request.")
            raise AuthError("No token")

        headers = {"Authorization": f"Token {key}"}
        link = f"https://plus.character.ai/{url}"
        if neo:
            link = link.replace("plus", "neo")

        data = data or {}

        session = Session()  # Create a session using curl_cffi

        try:
            self.logger.info(f"Sending {method} request to {link}")

            # Handle multipart requests
            if multipart:
                self.logger.debug("Handling multipart request")
                r = session.post(link, headers=headers, data=data, mime=multipart)
            elif method == "POST":
                r = session.post(link, headers=headers, json=data)
            elif method == "PUT":
                r = session.put(link, headers=headers, json=data)
            elif method == "GET":
                r = session.get(link, headers=headers)
            else:
                self.logger.error(f"Unsupported HTTP method: {method}")
                raise ValueError(f"Unsupported HTTP method: {method}")

            # Log response status
            self.logger.info(f"Received response: {r.status_code} from {link}")

            # Check for neo-specific errors
            if neo and not r.ok:
                self.logger.error(f"Neo request failed with response: {r.text}")
                try:
                    raise ServerError(r.json().get("comment", r.text))
                except KeyError:
                    raise ServerError(r.text)

            # Handle common HTTP errors
            if r.status_code == 404:
                self.logger.warning("Resource not found (404)")
                raise ServerError("Not Found")
            elif not r.ok:
                self.logger.error(f"Request failed with status code: {r.status_code}")
                raise ServerError(f"Server returned status code: {r.status_code}")

            # Handle and log JSON response parsing
            text = r.text
            if "}\n{" in text and split:
                self.logger.debug("Handling split response")
                text = "{" + text.split("}\n{")[-1]

            try:
                res = json.loads(text)
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON decoding error: {e}")
                raise JSONError(f"Unable to decode JSON. Server response: {r.text}")

            # Check for authentication or server errors in response
            if res.get("force_login"):
                self.logger.error("Authentication required (force_login)")
                raise AuthError("Authentication required")
            if res.get("status") != "OK" or res.get("abort"):
                error_message = res.get("error", "Unknown error")
                self.logger.error(f"Server returned an error: {error_message}")
                raise ServerError(error_message)
            if res.get("error"):
                self.logger.error(f"Server error: {res['error']}")
                raise ServerError(res["error"])

            return res

        except Exception as e:
            self.logger.error(f"Request failed: {e}")
            raise ServerError(f"Request failed: {e}")

        finally:
            self.logger.debug("Closing session")
            session.close()
