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


def addUser(username, password, role):
    cursor, conn = connect_mq()
    sql = f"insert into user (username,password,role) values ('{username}','{password}','{role}')"
    util.commitDB(conn=conn, cursor=cursor, sql=sql)


def getUserByName(username):
    cursor, conn = connect_mq()
    sql = f"select * from user where username='{username}';"
    util.commitDB(conn=conn, cursor=cursor, sql=sql, isRB=False)
    for i in cursor.fetchall():
        return User(i[0], i[1], i[2], i[3])


def setToken(uid, token):
    conn = connect_rd()
    conn.set(uid, token)
    conn.close()
