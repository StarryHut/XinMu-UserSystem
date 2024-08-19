from service import getIdByToken, getRoleById


def checkAdmin(token) -> bool:
    uid = getIdByToken(token)
    role = getRoleById(uid)
    if role == "admin":
        return True
    elif role == "user":
        return False
