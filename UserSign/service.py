import util
import dao
import time


def register(username, password, role):
    if not util.checkValid(username + password + role):
        """用户输入含非法字符"""
        return {"state": -1}
    if len(username) >= 10 or len(password) <= 10 or len(password) >= 15:
        """用户名过长或密码过短过长"""
        return {"state": -2}
    if dao.getUserByName(username=username) is not None:
        """用户名已存在"""
        return {"state": 0}
    else:
        """注册成功"""
        dao.addUser(username=username, password=password, role=role)
        return {"state": 1}


def login(username, password):
    if not util.checkValid(username + password):
        """用户输入含非法字符"""
        return {"state": 0}
    user = dao.getUserByName(username=username)
    if user is None:
        """该用户不存在(用户名错误)"""
        return {"state": -1}
    if password == user.password:
        """登录成功"""
        timestamp = str(time.time())
        token = util.createToken(user.username + user.password + user.role + timestamp)
        dao.setToken(user.uid, token)
        return {"token": token, "state": 1}
    else:
        """密码错误"""
        return {"state": -2}
