import sqlite3


def check_user(ChatId, UserId, UserName):
    db = sqlite3.connect(database='tgbot/services/DataBases/Users.db')
    sql = db.cursor()
    User = sql.execute(f'''SELECT UserId FROM "{ChatId}" WHERE UserId = {UserId}''').fetchall()
    if User:
        return True
    else:
        add_new_user(ChatId, UserId, UserName)


def mute(ChatId, UserId, UserName):
    db = sqlite3.connect(database='tgbot/services/DataBases/Users.db')
    sql = db.cursor()

    check_user(ChatId, UserId, UserName)

    User = sql.execute(f'''SELECT IsMuted, UserName FROM "{ChatId}" WHERE UserId = {UserId}''').fetchall()[0]

    if User[0] == 1:
        sql.close()
        del db, sql
        return 0
    else:
        sql.execute(f'''UPDATE "{ChatId}" SET IsMuted = 1, Warns = 0 WHERE UserId = "{UserId}" ''')
        db.commit()
        sql.close()
        del db, sql
        return 1


def unmute(ChatId, UserId, UserName):
    db = sqlite3.connect(database='tgbot/services/DataBases/Users.db')
    sql = db.cursor()

    check_user(ChatId, UserId, UserName)

    sql.execute(f'''UPDATE "{ChatId}" SET IsMuted = 0 WHERE UserId = "{UserId}" ''')
    db.commit()
    sql.close()
    del db, sql
    return 1


def warn(ChatId, UserId, UserName):
    db = sqlite3.connect(database='tgbot/services/DataBases/Users.db')
    sql = db.cursor()

    check_user(ChatId, UserId, UserName)

    warns = sql.execute(f'''SELECT Warns, IsMuted FROM "{ChatId}" WHERE UserId = {UserId}''').fetchall()[0]
    if warns[0] + 1 >= 3 and warns[1] == 0:
        sql.execute(f'''UPDATE "{ChatId}" SET Warns = 0, IsMuted = 1 WHERE UserId = "{UserId}"''')
        db.commit()
        sql.close()
        del sql
        return -1
    elif warns[0] == 0 and warns[1] == 1:
        return -2
    else:
        sql.execute(f'''UPDATE "{ChatId}" SET Warns = {warns[0] + 1} WHERE UserId = "{UserId}"''')
        db.commit()
        sql.close()
        del sql
        return warns[0] + 1


def unwarn(ChatId, UserId, UserName):
    db = sqlite3.connect(database='tgbot/services/DataBases/Users.db')
    sql = db.cursor()

    check_user(ChatId, UserId, UserName)

    sql.execute(f'''UPDATE "{ChatId}" SET Warns = {0} WHERE UserId = "{UserId}"''')
    db.commit()
    sql.close()
    del sql
    return 1


def add_new_user(ChanelId, UserId: int, UserName: str):
    db = sqlite3.connect(database='tgbot/services/DataBases/Users.db')
    sql = db.cursor()
    sql.execute(f'''INSERT INTO "{str(ChanelId)}" (UserId,UserName) VALUES ({UserId},"{UserName}")''')
    db.commit()
    sql.close()
    db.close()
    del sql


# При добавлении бота в чат пользователь должен прописать команду /Add_new_сhat что бы добавить чат в базу данных
def add_new_chat(chatId):
    db = sqlite3.connect('tgbot/services/DataBases/Users.db')
    sql = db.cursor()
    sql.execute(f'''CREATE TABLE IF NOT EXISTS "{chatId}" (
           UserId INTEGER PRIMARY KEY,
           UserName STRING NOT NULL,
           IsMuted INTEGER DEFAULT (0) NOT NULL,
           Warns INTEGER NOT NULL DEFAULT (0) 
           )
        ''')
    db.commit()
    sql.close()
    db.close()

    del sql
