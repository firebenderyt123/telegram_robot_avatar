# encoding: utf-8
from telethon.tl.types import UserStatusOffline, UserStatusOnline
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon import TelegramClient, sync
from telethon import events, types
from telethon import functions, types
from config import *
from utils import *
from datetime import datetime, timedelta
import asyncio
import emoji

# os.system('python generate_time_images.py')

client = TelegramClient('Session', api_id, api_hash)
client.start()

current_photo = ''
time_to_reaction = 30
next_date = datetime(1800, 1, 1)

online_photo = f"{path}photos/robot_default.png"
offline_photo = f"{path}photos/robot_dead.png"

photos = {
    '👍': f"{path}photos/robot_fun.png",
    '👌': f"{path}photos/robot_fun.png",
    '😱': f"{path}photos/robot_shock.png",
    '\u2764': f"{path}photos/robot_love.png", # сердце
    '😢': f"{path}photos/robot_cry.png",
    '👎': f"{path}photos/robot_cry.png",
    '🔥': f"{path}photos/robot_fun.png",
    '🥰': f"{path}photos/robot_love.png", # в сердечках
    '👏': f"{path}photos/robot_fun.png",
    '😁': f"{path}photos/robot_fun.png",
    '🤔': f"{path}photos/robot_default.png", # думает
    '🤯': f"{path}photos/robot_shock.png", # сносит крышу
    '🤬': f"{path}photos/robot_angry.png", # красный злой с матами
    '🎉': f"{path}photos/robot_fun.png",
    '🐳': f"{path}photos/robot_fun.png",
    '🤩': f"{path}photos/robot_fun.png", # звезды в глазах
    '🤮': f"{path}photos/robot_shit.png", # блевота
    '💩': f"{path}photos/robot_shit.png",
    '🙏': f"{path}photos/robot_fun.png", # спасибо (руки)
    '🕊': f"{path}photos/robot_fun.png", # голубь мира
    '🤡': f"{path}photos/robot_fun.png", # клоун
    '🥱': f"{path}photos/robot_default.png", # зевота
    '🥴': f"{path}photos/robot_default.png", # пьяный
    '😍': f"{path}photos/robot_love.png",
    '❤️‍🔥': f"{path}photos/robot_love.png",
    '🌚': f"{path}photos/robot_shock.png", # черная луна
    '🤣': f"{path}photos/robot_fun.png", # смех до слез на боку
}

def isCanChangePhoto(path):
    return current_photo != path

async def changePhoto(path):
    if not isCanChangePhoto(path):
        return False

    while datetime.now() < next_date:
        await asyncio.sleep(1)

    await client(DeletePhotosRequest(await client.get_profile_photos('me')))
    file = await client.upload_file(path)
    await client(UploadProfilePhotoRequest(file))
    current_photo = path

async def changePhotoReactions(reaction):
    photo = photos[reaction]
    if not isCanChangePhoto(photo):
        return False

    await changePhoto(photo)
    global next_date
    next_date = datetime.now() + timedelta(seconds=time_to_reaction)

@client.on(events.Raw)
async def handler(update):
    # print(update.stringify())
    if isinstance(update, types.UpdateEditChannelMessage):
        if update.message.from_id == None or update.message.from_id.user_id == admin_id:
            reaction = update.message.reactions.results[-1].reaction.encode("utf-8")
            await changePhotoReactions(reaction.decode('utf-8'))
    elif isinstance(update, types.UpdateEditMessage):
        if update.message.from_id == None or update.message.from_id.user_id == admin_id:
            reaction = update.message.reactions.results[-1].reaction.encode("utf-8")
            await changePhotoReactions(reaction.decode('utf-8'))

    elif isinstance(update, types.UpdateUserStatus):
        if update.user_id == admin_id:
            if isinstance(update.status, types.UserStatusOnline):
                await changePhoto(online_photo)
                # print(f"Went Online at : {datetime.now()}")
            elif isinstance(update.status, types.UserStatusOffline):
                await changePhoto(offline_photo)
                # print(f"Was recently online at : {datetime.now()}")

client.run_until_disconnected()