import web
from handle import Handle
import db
import time
import math

urls = (
    '/wx', 'Handle',
)


def init():
    Handle._standard_list = db.select_deck_name_by_meta(1)
    Handle._historic_list = db.select_deck_name_by_meta(2)
    Handle.deck_upd_ts = math.floor(time.time())


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

