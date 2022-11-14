import os

if 'DYNO' in os.environ:
    debug = False
    path = "/app/"
else:
    debug = True
    path = ""

api_id = ''
api_hash = ''

admin_id = 