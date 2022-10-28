import os

if 'DYNO' in os.environ:
    debug = False
    path = "/app/"
else:
    debug = True
    path = ""

api_id = '1049850'
api_hash = '5bfddfcb823e22c62719e3e2964c3be2'

admin_id = 435375091