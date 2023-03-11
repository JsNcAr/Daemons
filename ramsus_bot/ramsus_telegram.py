#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Simple Bot to send ip of personal server.

import asyncio

import logging

from telegram import Update

from telegram.ext import Application, CommandHandler, ContextTypes

import os

import datetime as dt

import requests

# Enable logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


# Define a few command handlers. These usually take the two arguments update and

# context.

# Best practice would be to replace context with an underscore,

# since context is an unused local variable.

# This being an example and not having context present confusing beginners,

# we decided to have it present as context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_html(
        "Hi! this bot sends you the ip of the server using <em>/send</em>.")


def ip() -> str:
    """Gets the ip of the server."""
    os.system("dig @resolver1.opendns.com myip.opendns.com +short > ip.txt")
    with open("ip.txt", "r") as ip_file:
        ip = str(ip_file.read())
    return ip


async def send_ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the ip of the server"""
    ip_ = ip()
    await update.message.reply_text(ip_)


def force_send_ip() -> None:
    """Send the ip of the server as a message"""
    ip_ = ip()
    token = "token"
    response = requests.post(
        url=f'https://api.telegram.org/bot{token}/sendMessage',
        data={
            'chat_id': "chat_id",
            'text': 'The IP has changed, the new IP is: ' + ip_
        }).json()


def main() -> None:
    """Run bot."""

    # Create the Application and pass it your bot's token.
    token = "token"
    application = (Application.builder().token(token).build())

    # on different commands - answer in Telegram

    application.add_handler(CommandHandler(["start", "help"], start))

    application.add_handler(CommandHandler("send", send_ip))

    application.run_polling()


if __name__ == "__main__":

    main()
