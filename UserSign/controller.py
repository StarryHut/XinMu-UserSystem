from fastapi import FastAPI
from request import Login, Register
import service
import uvicorn

app = FastAPI()


@app.post("/sign/register")
def register(request: Register):
    result = service.register(
        username=request.username,
        password=request.password,
        role=request.role
    )
    if result.get("state") == -1:
        return {"msg": "输入包含非法字符"}
    if result.get("state") == -2:
        return {"msg": "用户名不得超过10位,密码不得小于10位大于15位"}
    if result.get("state") == 0:
        return {"msg": "用户名已存在"}
    if result.get("state") == 1:
        return {"msg": "注册成功"}


@app.post("/sign/login")
def login(request: Login):
    result = service.login(
        username=request.username,
        password=request.password
    )
    if result.get("state") == 0:
        return {"msg": "输入包含非法字符", "islogin": False}
    if result.get("state") == -1:
        return {"msg": "用户名错误", "islogin": False}
    if result.get("state") == -2:
        return {"msg": "密码错误", "islogin": False}
    if result.get("state") == 1:
        return {"msg": "登陆成功", "islogin": True, "token": result.get("token")}


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
