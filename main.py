# encoding: utf-8
from telethon.tl.types import UserStatusOffline, UserStatusOnline
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon import TelegramClient, sync
from telethon import events
from config import *
from utils import *
from datetime import datetime
import time

# os.system('python generate_time_images.py')

client = TelegramClient('Session', api_id, api_hash)
client.start()

@client.on(events.UserUpdate)
async def my_event_handler(event):
    if event.user_id == admin_id:
        # print(event.user_id, admin_id, event)
        if event.online:
            client(DeletePhotosRequest(client.get_profile_photos('me')))
            file = client.upload_file(f"{path}photos/robot_default.png")
            client(UploadProfilePhotoRequest(file))
            # print(f"Went Online at : {datetime.now()}")
        elif event.recently:
            client(DeletePhotosRequest(client.get_profile_photos('me')))
            file = client.upload_file(f"{path}photos/robot_dead.png")
            client(UploadProfilePhotoRequest(file))
            # print(f"Was recently online at : {datetime.now()}")
        elif event.typing:
            print(f"Typed a message at : {datetime.now()}")
        else:
            print("Sorry there was an error.")
    else:
        pass

client.run_until_disconnected()