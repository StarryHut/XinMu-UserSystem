import dao
import util


def getAllUser():
    user = dao.getAllUser()
    if user is []:
        return {"msg": "暂无用户"}
    return [i.__dict__ for i in user]


def getUserByKw(kw):
    user = dao.getUserByKw(kw=kw)
    if user is None:
        return {"msg": "暂无匹配用户"}
    return [i.__dict__ for i in user]


def getIdByToken(token):
    return dao.getIdByToken(token)


def getRoleById(uid):
    user = dao.getRoleById(uid)
    return [i.__dict__ for i in user]


def getAllToken():
    token = dao.getAllToken()
    if token is []:
        return {"msg": "暂无用户"}
    return token


def addAdmin(username, password, role):
    dao.addAdmin(username, password, role)
    user = dao.getUserByName(username)
    conn = dao.connect_rd()
    conn.set(user.uid, util.createToken(user.username + user.password + user.role))


def delUserById(uid: int):
    dao.delUserById(uid=uid)
    dao.delToken(uid=uid)


def updateUserById(uid: int, username, password, role):
    dao.updateUserById(uid=uid, username=username, password=password, role=role)
