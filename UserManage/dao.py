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


def getUserByInfo(**info):
    cursor, conn = connect_mq()
    sql = f"select role from user where {list(info)[0]}='{info.get(list(info)[0])}';"
    util.commitDB(conn=conn, cursor=cursor, sql=sql, isRB=False)
    for i in cursor.fetchall():
        return User(i[0], i[1], i[2], i[3])


def addAdmin(username, password, role="admin"):
    cursor, conn = connect_mq()
    sql = f"insert into user (username,password,role) values ('{username}','{password}','{role}')"
    util.commitDB(conn=conn, cursor=cursor, sql=sql)


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


def getIdByToken(token):
    conn = connect_rd()
    for key in conn.scan_iter(count=100):
        if conn.get(key) == token:
            return key


def delToken(uid):
    conn = connect_rd()
    conn.delete(uid)
    conn.close()


def getAllToken():
    token_list = []
    conn = connect_rd()
    keys = conn.keys('*')
    for i in keys:
        token_list.append({i.decode(): conn.get(i).decode()})
    conn.close()
    return token_list
