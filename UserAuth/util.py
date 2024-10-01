import os
import hashlib
from dotenv import load_dotenv

load_dotenv()


def commitDB(conn, cursor, sql, isRB=True):
    """对数据库操作中的事务,回滚等操作进行封装"""
    conn.begin()
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        if isRB:
            conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def checkValid(_input: str) -> bool:
    legal_char = os.getenv("ILLEGAL_CHARACTER").split(",")
    flag = True
    for c in list(_input):
        if c in legal_char:
            flag = False
            break
    return flag


def createToken(info: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(info.encode())
    hex_digest = sha256.hexdigest()
    return hex_digest


def addHash(data: str) -> str:
    return createToken(info=data)
