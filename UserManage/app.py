from fastapi import FastAPI
import service
import uvicorn
from request import UpdateUserById
from gateway import checkAdmin
app = FastAPI()


@app.middleware("http")
async def gateway(request, call_next):
    token = request.headers.get("token")
    if checkAdmin(token) is False:
        return "{'msg':'你是普通用户,滚!!!'}"
    response = await call_next(request)
    return response


@app.get("/manage/getUserByKw/{kw}")
def getUserByKw(kw: str):
    return service.getUserByKw(kw=kw)


@app.get("/manage/getAllUser")
def getAllUser():
    return service.getAllUser()


@app.get("/manage/getAllToken")
def getAllToken():
    return service.getAllToken()


@app.post("/manage/addAdmin")
def addAdmin(request):
    service.addAdmin(
        username=request.username,
        password=request.password,
        role=request.role
    )


@app.get("/manage/delUserById/{uid}")
def delUserById(uid: int):
    service.delUserById(uid)
    return {"msg": "用户删除成功"}


@app.post("/manage/updateUserById")
def updateUserById(request: UpdateUserById):
    service.updateUserById(
        uid=request.uid,
        username=request.username,
        password=request.password,
        role=request.role
    )
    return {"msg": "用户信息更新成功"}


if __name__ == "__main__":
    uvicorn.run(app, port=8081)
