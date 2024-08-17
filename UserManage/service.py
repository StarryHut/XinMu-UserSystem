import dao


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


def delUserById(uid: int):
    dao.delUserById(uid=uid)
    dao.delToken(uid=uid)


def updateUserById(uid: int, username, password, role):
    dao.updateUserById(uid=uid, username=username, password=password, role=role)
