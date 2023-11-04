""" This module Represents a WhatsApp bot manager that provides an entry point
for external users to interact with the WhatsApp API.
"""

import json
import os
from typing import Callable, Any
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from uvicorn import Config, Server
from starlette.requests import Request
from starlette.responses import Response

from whatsapp._files.message import Message

from whatsapp._validators.server import Webhook

from whatsapp.bot import Bot


load_dotenv()


class Whatsapp:
    # pylint: disable=line-too-long

    """
    Represents a WhatsApp bot manager that provides an entry point for external
     users to interact with the WhatsApp API.

    Args:
        cloud_api_access_token (str, optional): The Cloud API access token used for authentication.
        wa_phone_number_id (str, optional): The WhatsApp phone number ID.
        version (str, optional): The WhatsApp API version to use.

    Attributes:
        verify_token (str): Verification token for webhook authentication.
        __app (FastAPI): FastAPI instance for handling incoming requests.
        __router (APIRouter): APIRouter for defining routes.
        bot (Bot): Instance of the Bot class for WhatsApp API communication.

    Methods:
        - __callback_func(callback: Callable[[[Message]], None]): Set the callback
         function for handling incoming
         messages.
        - __server(request: Request): Internal method to process incoming requests and messages.
        - run_server(callback: Callable[[Request, Message], Union[Response, None],
         webhook_url: str = "/webhook",port: int = 8000, verify_token: str = None): Start the FastAPI server to
          handle incoming webhooks.

    Usage Example:
    ```
    from your_library import Whatsapp

    # Initialize the Whatsapp manager
    whatsapp = Whatsapp(cloud_api_access_token="your_access_token",
     wa_phone_number_id="your_phone_number_id",
    version="v17.0")

    # Define a callback function to handle incoming messages
    def handle_message(request, message):
        # Your message handling logic here...

    # Run the FastAPI server
    whatsapp.run_server(callback=handle_message, webhook_url="/webhook", port=8000, verify_token="your_verify_token")
    ```
    """

    def __init__(
        self,
        cloud_api_access_token: str = None,
        wa_phone_number_id: str = None,
        version: str = None,
    ):
        """
        Initialize a Whatsapp instance for managing WhatsApp bot interactions.

        Args:
            cloud_api_access_token (str, optional): The Cloud API access token used for authentication.
            wa_phone_number_id (str, optional): The WhatsApp phone number ID.
            version (str, optional): The WhatsApp API version to use.

        """

        self.verify_token: str = ""
        self.__app = FastAPI()
        self.__router = APIRouter()
        self.bot = Bot(
            cloud_api_access_token=cloud_api_access_token,
            wa_phone_number_id=wa_phone_number_id,
            version=version,
        )
        self.__server: Server = Server(
            config=Config(host="0.0.0.0", port=8000, app=self.__app)
        )
        self.__callback_func = None

    def __set_callback_func(self, callback: Callable[[[Message]], None]):
        """
        Set the callback function for handling incoming messages from the whatsapp api.

        Args:
            callback (Callable[[[Message]], None]): The callback function to handle incoming messages.
        """
        validator = Webhook(callback=callback)
        self.__callback_func: Callable = validator.callback

    async def __handler(self, request: Request):
        """
        Internal method to process incoming requests and messages.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            Response: The HTTP response.
        """

        if request.method == "GET":
            mode = request.query_params.get("hub.mode")
            challenge = request.query_params.get("hub.challenge")
            verify_token = request.query_params.get("hub.verify_token")

            if verify_token == self.verify_token and mode == "subscribe":
                return Response(challenge)

        data = await request.json()

        message = Message.de_json(data=data, bot=self.bot)

        if message:
            await self.__callback_func(request, message)

            await message.mark_message_as_read()

        return Response(json.dumps(({"status": "success"})))

    async def stop_server(self):
        """
        Stop the FastAPI sever that is accepting webhook requests.

        Raises:
            RuntimeError: if the server is not started

        """
        if not self.__server.started:
            raise RuntimeError("Server is not started!")

        await self.__server.shutdown()

    def run_server(
        self,
        callback: Callable[[Request, Message], Any],
        webhook_url: str = "/webhook",
        port: int = 8000,
        verify_token: str = None,
    ):
        """
        Start the FastAPI server to handle incoming webhooks.

        Args:
            callback (Callable[[Request, Message], Union[Response, None]]): The callback function to handle incoming
             messages.
            webhook_url (str, optional): The URL endpoint for webhooks (default is "/webhook").
            port (int, optional): The port on which the FastAPI server should run (default is 8000).
            verify_token (str, optional): The verification token for webhook authentication.

        Raises:
            RuntimeError: If the callback function or verify token is not provided.

        Example:

        def handle_message(request: Request, message:Message):
            print(message.type)

        whatsapp.run_server(callback=handle_message, webhook_url="/webhook", port=8000, verify_token="your_verify_token"
        )

        """

        if not verify_token:
            verify_token = os.getenv("WA_VERIFY_TOKEN")

        if not isinstance(callback, Callable):
            raise RuntimeError("A callback function is expected to be passed!")

        if not verify_token:
            raise RuntimeError(
                "Either configure verify token in env file like this: WA_VERIFY_TOKEN or pass it as an argument!"
            )

        self.verify_token = verify_token

        if not webhook_url.startswith("/"):
            webhook_url = "/" + webhook_url

        self.__set_callback_func(callback=callback)

        self.__router.add_route(
            webhook_url, endpoint=self.__handler, methods=["POST", "GET"]
        )

        self.__app.include_router(self.__router)

        #  register a handler that handles all exceptions that occurs in the handler pipline
        @self.__app.exception_handler(Exception)
        def handle(req: Request, exc):
            """this would still throw an exception while still returning a response to the whatsapp
            API immediately, so it doesn't resend the request again"""

            print(req, exc)

            return Response("true")

        print(f"Webhook Url: localhost:{port}{webhook_url}")

        config = Config(host="0.0.0.0", port=port, app=self.__app)
        server = Server(config)

        self.__server = server
        self.__server.run()
