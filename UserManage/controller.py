from fastapi import FastAPI
import service
import uvicorn
from request import UpdateUserById
app = FastAPI()


@app.get("/getUserByKw/{kw}")
def getUserByKw(kw: str):
    return service.getUserByKw(kw=kw)


@app.get("/getAllUser")
def getAllUser():
    return service.getAllUser()


@app.post("/delUserById/{uid}")
def delUserById(uid: int):
    service.delUserById(uid)
    return {"msg": "用户删除成功"}


@app.post("/updateUserById")
def updateUserById(request: UpdateUserById):
    service.updateUserById(
        uid=request.uid,
        username=request.username,
        password=request.password,
        role=request.role
    )
    return {"msg": "用户信息更新成功"}


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
