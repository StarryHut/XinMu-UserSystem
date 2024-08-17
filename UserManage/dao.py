import dotenv
import os
import pymysql
import redis
import util
from model import User

dotenv.load_dotenv()


def connect_mq():
    conn = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_DATABASE")
    )
    cursor = conn.cursor()
    return cursor, conn


def connect_rd():
    return redis.Redis(
        host=os.getenv("RD_HOST"),
        port=int(os.getenv("RD_PORT")),
        password=os.getenv("RD_PASSWORD")
    )


def getAllUser():
    user_list = []
    cursor, conn = connect_mq()
    sql = "select * from user;"
    util.commitDB(conn=conn, cursor=cursor, sql=sql, isRB=False)
    for i in cursor.fetchall():
        user_list.append(User(i[0], i[1], i[2], i[3]))
    return user_list


def getUserByKw(kw):
    user_list = []
    cursor, conn = connect_mq()
    sql = f"select * from user where username like '%{kw}%' or password like '%{kw}%';"
    util.commitDB(conn=conn, cursor=cursor, sql=sql, isRB=False)
    for i in cursor.fetchall():
        user_list.append(User(i[0], i[1], i[2], i[3]))
    return user_list


def delUserById(uid: int):
    cursor, conn = connect_mq()
    sql = f"delete from user where uid='{uid}'"
    util.commitDB(conn=conn, cursor=cursor, sql=sql)


def updateUserById(uid: int, username, password, role):
    user = User(uid, username, password, role)
    cursor, conn = connect_mq()
    sql = f"update user set username='{user.username}', password='{user.password}', role='{user.role}' " \
          f"where uid={user.uid}"
    util.commitDB(conn=conn, cursor=cursor, sql=sql)


def delToken(uid):
    conn = connect_rd()
    conn.delete(uid)
    conn.close()

