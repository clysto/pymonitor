# PyMonitor

A python framework that makes it more convenient for you to build websocket applications!

## Demo

```py
from pymonitor import PymonitorEvent, Pymonitor
import asyncio


async def main():
    app.on("a", print)
    count = 1
    while True:
        await asyncio.sleep(1)
        await app.emit(PymonitorEvent("time", {"count": count}))
        count += 1


app = Pymonitor(main)
```
