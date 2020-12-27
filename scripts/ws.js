const WebSocket = require('ws');

const ws = new WebSocket('ws://localhost:8000/ws');

ws.on('open', () => {
  console.log('open');
  ws.send(
    JSON.stringify({
      type: 'msg',
      payload: {
        hello: 'world',
      },
    })
  );
});

ws.on('message', (data) => {
  console.log(data);
});
