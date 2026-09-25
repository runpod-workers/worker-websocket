# Serverless WebSocket Worker Example 

This WebSocket worker example allows direct communication with a serverless worker without using Runpod’s default REST API. It enables real-time, bidirectional communication between a websocket client and the worker.

## How It Works

1. Wake up the worker – You must send a request(`https://api.runpod.ai/v2/endpointId/run`) to wake up the serverless worker.
2. Retrieve the worker’s `public IP` and `TCP port` – Once the worker is awake, `handler` [function](https://github.com/runpod-workers/worker-websocket/blob/main/rp_handler.py#L52) will obtain worker's public IP and TCP port from the environment variables.
3. Share connection details – Use [progress_update](https://docs.runpod.io/serverless/workers/handlers/handler-additional-controls#update-progress) to share the public IP and TCP port with any backend application that plans to communicate with the worker.
4. Fetch connection details – Call `https://api.runpod.ai/v2/endpointId/status/request_id` to retrieve the public IP and TCP port.
5. Establish a WebSocket connection – Use a [WebSocket client](https://github.com/runpod-workers/worker-websocket/blob/main/client.py) to connect to the worker using the obtained IP and port.
6. Complete communication and shut down – Once the client or backend application is done, send a [shutdown signal](https://github.com/runpod-workers/worker-websocket/blob/main/client.py#L13), in this example, we are transmitting the string “shutdown”.
7. Graceful termination – Upon receiving "shutdown", the WebSocket server will [shut down](https://github.com/runpod-workers/worker-websocket/blob/main/rp_handler.py#L19), the handler function will return, and the worker instance will be terminated.

### Important Deployment Notes

- After deploying this code, remember to go to Serverless Settings → Docker Configuration → Expose TCP Ports and expose port 8765, or whichever port your WebSocket server is running on.
- If you choose a different port, ensure that you update the [environment variable name](https://github.com/runpod-workers/worker-websocket/blob/main/rp_handler.py#L53) accordingly, as the exposed port number is appended to the variable name.

