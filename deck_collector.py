import mtgazone_crawler
import db
import time
import math

# 1 standard 2 historic


# source, deck_name, deck_code, deck_meta, deck_color, create_dt, create_ts
def mtgazone_decks_collector():
    source = "mtgazone"
    today_dt = time.strftime("%Y%m%d", time.localtime())
    deck_color = 00000

    def insert_mtgazone_decks_to_db(deck_list, deck_meta):
        for deck in deck_list:
            deck_name = deck[0]
            deck_url = deck[1]
            deck_code = mtgazone_crawler.get_deck_code_by_details_url(deck_url).replace("'", "''")
            # print(deck_code)
            create_ts = math.floor(time.time())
            db.insert_deck(source, deck_name, deck_code, deck_meta, deck_color, today_dt, create_ts)
            time.sleep(0.1)
        db.commit_all()


    standard_decks = mtgazone_crawler.get_decks_by_format(mtgazone_crawler.STANDARD)[::-1]
    insert_mtgazone_decks_to_db(standard_decks, 1)
    
    historic_decks = mtgazone_crawler.get_decks_by_format(mtgazone_crawler.HISTORIC)[::-1]
    insert_mtgazone_decks_to_db(historic_decks, 2)

    cur_tm = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    print("%s MTGAZone套牌更新" % cur_tm)


def decks_collect():
    while True:
        mtgazone_decks_collector()
        time.sleep(14400)


decks_collect()


# mtgazone_decks_collector()
