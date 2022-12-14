import uvicorn
import socketio
from fastapi import FastAPI

def handle_connect(sid, environ):
    pass

class SocketManager:
    def __init__(self, origins: list[str]):
        self.server = socketio.AsyncServer(
            cors_allowed_origins=origins,
            async_mode="asgi",
            logger=True,
            engineio_logger=True,
        )
        self.app = socketio.ASGIApp(self.server)

    @property
    def on(self):
        return self.server.on

    @property
    def send(self):
        return self.server.send

    def mount_to(self, path: str, app: socketio.ASGIApp):
        app.mount(path, self.app)

socket_manager = SocketManager(["*"]) # do this better
socket_manager.on("connect", handler=handle_connect)

app = FastAPI()
socket_manager.mount_to("/ws", app)

if __name__ == "__main__":
    kwargs = {"host": "0.0.0.0", "port": 80}
    kwargs.update({"reload": True})
    uvicorn.run("server:app", **kwargs)