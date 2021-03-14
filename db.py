import sqlite3

INSERT_DECK = '''
insert into deck_info (source, deck_name, deck_code, deck_meta, deck_color, create_dt, create_ts) 
values('%s', '%s', '%s', %s, %s, '%s', %s)'''
SELECT_DECK_NAME_LIST_BY_META = '''
select deck_name, deck_code from deck_info where deck_meta = '%s' order by create_ts desc limit 40'''
conn = sqlite3.connect('mtgtool.db')
c = conn.cursor()


def insert_data_to_table(table, data):
    pass


# source string, code string, create_dt 20210101, create_ts timestamp
def insert_deck(source, deck_name, deck_code, deck_meta, deck_color, create_dt, create_ts):
    sql = INSERT_DECK % (source, deck_name, deck_code, deck_meta, deck_color, create_dt, create_ts)
    # print(sql)
    c.execute(sql)


def select_deck_name_by_meta(deck_meta):
    sql = SELECT_DECK_NAME_LIST_BY_META % deck_meta
    cursor = c.execute(sql)
    decks = []
    for row in cursor:
        deck_name = row[0]
        deck_code = row[1]
        decks.append((deck_name, deck_code))

    return decks



def execute_sql(sql):
    c.execute(sql)


def commit_all():
    conn.commit()


# c.execute("drop table deck_info;")
# c.execute('''
# create table deck_info
# (id INTEGER PRIMARY Key AUTOINCREMENT,
# source TEXT ,
# deck_name TEXT not null,
# deck_code TEXT not null,
# deck_meta TEXT not null,
# deck_color INT ,
# create_dt CHAR(8) not null,
# create_ts INT not null
# );
# ''');
# conn.commit()
# conn.close()
