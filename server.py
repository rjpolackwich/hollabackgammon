import uvicorn
import socketio
from fastapi import FastAPI

from bson.objectid import ObjectId

global registered
registered = dict()


sio = socketio.AsyncServer(
    cors_allowed_origins="http://localhost:4000",
    async_mode="asgi",
    logger=True,
    engineio_logger=True,
    )
socket_app = socketio.ASGIApp(sio)
app = FastAPI()

app.mount("/", socket_app)

@sio.on("login")
async def login(sid, data):
    print(data)
    username = data["username"]
    password = data["password"]
    if username in registered:
        if registered["username"]["password"] == password:
            await sio.emit("loginSuccess", registered["username"])
    else:
        await sio.emit("loginError", "not registered")


@sio.on("register")
async def register(sid, data):
    print(data)
    oid = ObjectId()
    username = data["username"]
    registered[username] = {
        "_id": str(oid),
        "_email": data["email"],
        "_password": data["password"]
    }
    await sio.emit("registerSuccess", "yay")

if __name__ == "__main__":
    kwargs = {"host": "0.0.0.0", "port": 4000}
    kwargs.update({"reload": True})
    uvicorn.run("server:app", **kwargs)