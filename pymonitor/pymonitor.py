from typing import Dict, Callable, List
from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute
from starlette.websockets import WebSocket, WebSocketState
import asyncio


class PymonitorEvent:
    def __init__(self, name: str, payload: Dict = None):
        self.name = name
        self.payload = payload


class Pymonitor(Starlette):
    def __init__(self, main):
        routes = [
            WebSocketRoute("/ws", self._ws),
        ]
        self.main = main
        self.clients: List[WebSocket] = []
        self.handlers: Dict[str, List[Callable]] = {}
        super().__init__(
            debug=True,
            routes=routes,
            on_startup=[self._on_startup],
        )

    async def _ws(self, websocket: WebSocket):
        await websocket.accept()
        try:
            self.clients.append(websocket)
            while True:
                msg = await websocket.receive_json()
                self._distribute_event(msg)
        except:
            await websocket.close()
            self.clients.remove(websocket)

    async def emit(self, event: PymonitorEvent):
        for client in self.clients:
            await client.send_json({"type": event.name, "payload": event.payload})

    def _on_startup(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.main())

    def on(self, name: str, handler: Callable):
        if name not in self.handlers:
            self.handlers[name] = []
        self.handlers[name].append(handler)

    def _distribute_event(self, msg):
        name = msg["type"] if "type" in msg else None
        payload = msg["payload"] if "payload" in msg else None
        if not name or name not in self.handlers:
            return
        for handler in self.handlers[name]:
            handler(payload)
