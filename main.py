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

from Queue import Queue

# os.system('python generate_time_images.py')

client = TelegramClient('Session', api_id, api_hash)
client.start()

current_photo = ''
time_to_reaction = 10
next_date = datetime(1800, 1, 1)

online_photo = f"{path}photos/robot_watermelon.png"
offline_photo = f"{path}photos/robot_dead.png"

loggedIn = False
isPhotoProccessRunning = False

queue = Queue()

photos = {
    '👍': f"{path}photos/robot_like.png",
    '👌': f"{path}photos/robot_fun.png",
    '😱': f"{path}photos/robot_shock.png",
    '\u2764': f"{path}photos/robot_love.png", # сердце
    '😢': f"{path}photos/robot_cry.png",
    '👎': f"{path}photos/robot_cry.png",
    '🔥': f"{path}photos/robot_fire.png",
    '🥰': f"{path}photos/robot_love.png", # в сердечках
    '👏': f"{path}photos/robot_fun.png",
    '😁': f"{path}photos/robot_fun.png",
    '🤔': f"{path}photos/robot_thinking.png", # думает
    '🤯': f"{path}photos/robot_boom.png", # сносит крышу
    '🤬': f"{path}photos/robot_angry.png", # красный злой с матами
    '🎉': f"{path}photos/robot_congratulation.png",
    '🐳': f"{path}photos/robot_water.png",
    '🤩': f"{path}photos/robot_star.png", # звезды в глазах
    '🤮': f"{path}photos/robot_foo.png", # блевота
    '💩': f"{path}photos/robot_shit.png",
    '🙏': f"{path}photos/robot_fun.png", # спасибо (руки)
    '🕊': f"{path}photos/robot_fun.png", # голубь мира
    '🤡': f"{path}photos/robot_joker.png", # клоун
    '🥱': f"{path}photos/robot_sleep.png", # зевота
    '🥴': f"{path}photos/robot_beer.png", # пьяный
    '😍': f"{path}photos/robot_love.png",
    '❤️‍🔥': f"{path}photos/robot_love.png",
    '🌚': f"{path}photos/robot_dark_moon.png", # черная луна
    '🤣': f"{path}photos/robot_fun.png", # смех до слез на боку
    '🌭': f"{path}photos/robot_hot_dog.png", # хот дог
    '💯': f"{path}photos/robot_100.png",
    '\u26a1': f"{path}photos/robot_zap.png", # zap
    '🍌': f"{path}photos/robot_banana.png",
    '🖕': f"{path}photos/robot_fuck.png", # fuck you
    '😈': f"{path}photos/robot_chert.png",
}

def isCanChangePhoto(path):
	global current_photo
	return current_photo != path and path != None

async def changePhoto():
    global isPhotoProccessRunning, time_to_reaction
    global next_date, loggedIn, current_photo

    if isPhotoProccessRunning:
        return False

    isPhotoProccessRunning = True
    path = queue.get_elem()
    if not isCanChangePhoto(path):
        queue.remove_elem()
        isPhotoProccessRunning = False
        return False

    # print(path, datetime.now())
    while datetime.now() < next_date:
        await asyncio.sleep(1)

    await client(DeletePhotosRequest(await client.get_profile_photos('me')))
    file = await client.upload_file(path)
    await client(UploadProfilePhotoRequest(file))
    current_photo = path
    queue.remove_elem()
    
    if current_photo != offline_photo and current_photo != online_photo:
        next_date = datetime.now() + timedelta(seconds=time_to_reaction)

    isPhotoProccessRunning = False

    if queue.get_length() > 0:
        await changePhoto()
    elif current_photo != offline_photo and current_photo != online_photo:
    	if loggedIn:
    		await setOnline()
    	else:
    		await setOffline()

async def changePhotoReactions(reaction):
    photo = photos[reaction]
    if not isCanChangePhoto(photo):
        return False

    if queue.get_length() > 0 and (queue.get_elem(-1) == offline_photo or queue.get_elem(-1) == online_photo):
        queue.insert(-1, photo)
    else:
        queue.push_back(photo)
    await changePhoto()

async def setOnline():
	global loggedIn
	if offline_photo in queue.get_queue():
		queue.replace(offline_photo, online_photo)
	elif online_photo not in queue.get_queue():
		queue.push_back(online_photo)
	loggedIn = True
	await changePhoto()

async def setOffline():
	global loggedIn
	if online_photo in queue.get_queue():
		queue.replace(online_photo, offline_photo)
	elif offline_photo not in queue.get_queue():
		queue.push_back(offline_photo)
	loggedIn = False
	await changePhoto()

@client.on(events.Raw)
async def handler(update):
    # print(update.stringify())
    if isinstance(update, types.UpdateEditChannelMessage):
        if update.message.from_id and update.message.from_id.user_id == admin_id:
            reaction = update.message.reactions.results[0].reaction.encode("utf-8")
            await changePhotoReactions(reaction.decode('utf-8'))
    elif isinstance(update, types.UpdateEditMessage):
        print(update.message.reactions.results)
        if update.message.from_id and update.message.from_id.user_id == admin_id:
            reaction = update.message.reactions.results[0].reaction.encode("utf-8")
            await changePhotoReactions(reaction.decode('utf-8'))

    elif isinstance(update, types.UpdateUserStatus):
        if update.user_id == admin_id:
            if isinstance(update.status, types.UserStatusOnline):
                await setOnline()
                # print(f"Went Online at : {datetime.now()}")
            elif isinstance(update.status, types.UserStatusOffline):
                await setOffline()
                # print(f"Was recently online at : {datetime.now()}")

client.run_until_disconnected()