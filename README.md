# WhatsApp Python SDK

Your go-to wrapper for simplifying WhatsApp Cloud API integration. 
The best python unofficial library written for the [Whatsapp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api/overview)

<img src="https://res.cloudinary.com/dkhelyskt/image/upload/v1697411070/whatsapp_logo_insxtu.png" alt="Whatsapp Logo" width="120" height="120">

## Project Information

[![Python Version](https://img.shields.io/badge/Python-3.7.2|3.8|3.9|3.10-blue.svg)](https://www.python.org/)
[![Pylint](https://github.com/t-ega/Whatsapp-Python-SDK/actions/workflows/pylint.yml/badge.svg)](https://github.com/t-ega/Whatsapp-Python-SDK/actions/workflows/pylint.yml)
[![Libraries Used](https://img.shields.io/badge/Dependencies-requests%20%7C%20FastAPI%20|Uvicorn-blue)]()
[![License](https://img.shields.io/badge/License-GNU-green)]([https://link-to-license](https://github.com/t-ega/Whatsapp-Python-SDK/blob/main/LICENSE))
[![Maintainer](https://img.shields.io/badge/Maintainer-Akpojiyovwi%20Tega-blue)](https://github.com/t-ega)
[![Documentation](https://img.shields.io/badge/Documentation-Link-blue)](https://github.com/t-ega/Whatsapp-Python-SDK/)

## Table of Contents
- [Introduction](#introduction)
- [Acknowledgements](#acknowledgements)
- [Prerequisites](#prerequisites)
- [Whatsapp Cloud API Support](#whatsapp-cloud-api-support)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Basic Usage](#basic-usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The WhatsApp Python SDK is a Python library that provides a comprehensive solution for managing WhatsApp Cloud interactions using the WhatsApp Cloud API. It allows you to send various types of messages, mark messages as read, and handle incoming webhooks. The library is designed to be flexible and can be easily integrated into your Python projects.
This module is meant to be purely used with python async and await.
This is the v1 of this open source project so not all whatsapp cloud features are currently supported. If you need any feature to be added please open a feature request!

Key Features:
- Send text messages with or without buttons
- Send image, audio, video, document, location, contact, and sticker messages
- Receive and process incoming messages via webhooks
- Set up a callback function to handle incoming messages
- Easy-to-use and customizable and lot more!


## Acknowledgements
 - God first of all.
 - [Whatsapp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api/overview)

## Authors

- [@Akpojiyovwi Tega(Me)](https://www.github.com/t-ega)

 
## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.7+
- [FastAPI](https://fastapi.tiangolo.com/)
- [uvicorn](https://www.uvicorn.org/)
- WhatsApp API Cloud Access Token (obtained from WhatsApp)
- Basic understanding of how the Whatsapp API works

## Whatsapp Cloud API Support

- The following types of the Whatsapp Cloud API v17.0 are supported.

# Normal messages
- send text
- send contact message
- send reaction messages
  
# Link messages
- send audio via link
- send image via link
- send video via link
- send document via link
- send sticker via link

# Reply to a user message using link
- send reply to message using an audio link
- send reply to message using an image link
- send reply to message using a video link
- send reply to message using a document link
- send reply to message using a reaction link

# Reply to a user messages
- send reply with a text

## Installation
You can install or upgrade `whatsapp-cloud-sdk` via:

```bash
$ pip install whatsapp-cloud-sdk --upgrade
```

You can also install directly from the repo, though this is usually not necessary.
```bash
$ git clone https://github.com/t-ega/whatsapp-cloud-sdk
$ cd whatsapp-cloud-sdk
$ pip install poetry
$ poetry install
```

## Getting Started

- Set Up Environment Variables

To run this project, you will need to add the following environment variables to your .env file
Otherwise you would need to pass it as an argument to the `whatsapp` class.

`CLOUD_API_ACCESS_TOKEN`

`WA_PHONE_NUMBER_ID`

`WA_VERSION='v17.0'`

- Import the necessary classes and modules:

```python

from whatsapp_cloud_sdk import WAManager
from whatsapp_cloud_sdk import Bot

# Create a WhatsApp manager instance

whatsapp = WAManager(cloud_api_access_token="your_access_token", wa_phone_number_id="your_phone_number_id",
                     version="v17.0")


# Set up a callback function to handle incoming messages:

# **NOTE: The callback function must be an asynchronous function!**

async def handle_message(request: Request, message: Message):
    print(message.type)
```

Start the FastAPI server to handle incoming webhooks:

```python
whatsapp.run_server(callback=handle_message, webhook_url="/webhook", port=8000, verify_token="your_verify_token")
```

## Basic Usage

- Receive and handle incoming messages in the callback function:

```python
async def handle_message(request: Request, message: Message):
    print("Received a message of type:", message.type)
    # Your custom logic to handle the incoming message
    # reply to the message recieved
    await message.reply_text(text="This is a reply")
```  

Send text messages:

```python
whatsapp.bot.send_text("Hello, world!", "recipient_number")
```

Send text messages with a list of dict buttons:

```python
buttons = [
    {"title": "Option 1", "id": "option1"},
    {"title": "Option 2", "id": "option2"},
]

await whatsapp.bot.send_text_with_buttons("Choose an option:", buttons, "recipient_number")
```

Send other types of messages (image, audio, video, etc.):

- Send an image by URL

```python
await whatsapp.bot.send_image_by_url("https://example.com/image.jpg", "Image caption", "recipient_number")
```

- Send a reply to a message recieved
  
```python

async def handle_message(request: Request, message: Message):
    await message.reply_text(text="Heyy")
```

- Get the type of message that was received

```python
async def handle_message(request: Request, message: Message):
    print("Received a message of type:", message.type)
```

- Mark a message as read (although this is done automatically by the bot)

```python
async def handle_message(request: Request, message: Message):
    await message.mark_as_read()
```
    
For more details on available methods and usage, refer to the documentation(in progress).

## Help
Currently this project is only maintained by me, I am looking forward to accepting pull requests. If you need help just open an issue
I would try my best to attend to all issues. 

## Inspiration
This project was inspired by the [Whastpp Nodejs SDK](https://github.com/WhatsApp/WhatsApp-Nodejs-SDK). Furthermore it was also inspired by the [Python Telegram Bot wrapper](https://github.com/python-telegram-bot/python-telegram-bot)

# Contributing
Contributions are welcome! Please see the Contribution Guidelines for more information.You can also help by reporting bugs or feature requests.

# License
You may copy, distribute and modify the software provided that modifications are described and licensed for free under LGPL-3. Derivatives works (including modifications or anything statically linked to the library) can only be redistributed under LGPL-3, but applications that use the library don't have to be.

# Disclaimer
This module is not officially affiliated with WhatsApp or Facebook. It's an independent project developed by the community.

Note:
For more detailed information about the methods and classes provided by the whatsapp-cloud-api module, refer to the module's source code or docstrings.