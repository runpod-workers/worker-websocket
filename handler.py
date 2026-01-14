from websocket_server import WebsocketServer
import runpod
import os

shutdown_flag = False  # Flag to track when to stop the server

def on_new_client(client, server):
    """Handle new client connection."""
    print(f"New client connected: {client['id']}")

def on_message(client, server, message):
    """Handle incoming messages from clients."""
    global shutdown_flag

    print(f"Received: {message}")
    server.send_message(client, f"Echo: {message}")

    # If the client sends "shutdown", set flag and close server
    if message.strip().lower() == "shutdown":
        print("Shutdown command received. Stopping WebSocket server...")
        shutdown_flag = True
        server.shutdown()  # Gracefully stop the WebSocket server

def on_client_left(client, server):
    """Handle client disconnection."""
    print(f"Client {client['id']} disconnected")

def start_websocket():
    """Start WebSocket server and wait for shutdown."""
    global shutdown_flag

    server = WebsocketServer(host="0.0.0.0", port=8765)
    server.set_fn_new_client(on_new_client)
    server.set_fn_client_left(on_client_left)
    server.set_fn_message_received(on_message)

    print("WebSocket server started on port 8765...")

    try:
        while not shutdown_flag:  # Keep running until shutdown is triggered
            server.run_forever()  # Blocking call, but allows shutdown handling
    except KeyboardInterrupt:
        print("WebSocket server manually stopped.")
    finally:
        print("WebSocket server has been shut down.")

    return "WebSocket server stopped successfully"  # Return handler response

def handler(event):
    """RunPod job handler that runs the WebSocket server and waits for shutdown."""

    public_ip = os.environ.get('RUNPOD_PUBLIC_IP', 'localhost')  
    tcp_port = int(os.environ.get('RUNPOD_TCP_PORT_8765', '8765')) 
    
    print(f"Public IP: {public_ip}")  
    print(f"TCP Port: {tcp_port}")  

    runpod.serverless.progress_update(event, f"Public IP: {public_ip}, TCP Port: {tcp_port}")

    # Start WebSocket server and wait for shutdown message
    result = start_websocket()

    return {
        "message": result,
        "public_ip": public_ip,
        "tcp_port": tcp_port
    }

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})