# Import the necessary libraries
import socket
import threading

# Define the IP address and port number of the server
IP = input("Enter a IP:")
PORT = 8080

print("connecting to", IP, "on port", PORT)


# Define a function to receive and handle messages from a client
def handle_client(client_socket, client_address):
    # Receive the client's name
    name = client_socket.recv(1024).decode()
    print(f"{name} has joined the chat")

    # Broadcast the client's name to all connected clients
    broadcast(f"{name} has joined the chat", client_socket)

    # Set the client's socket to be non-blocking
    client_socket.setblocking(False)

    # Continuously receive messages from the client
    while True:
        try:
            # Receive the client's message
            message = client_socket.recv(1024).decode()

            # If the client has sent an empty message, assume they have disconnected
            if not message:
                print(f"{name} has left the chat")

                # Broadcast the client's disconnection to all connected clients
                broadcast(f"{name} has left the chat", client_socket)

                # Close the client's socket
                client_socket.close()
                break
            else:
                # Broadcast the client's message to all connected clients
                broadcast(f"{name}: {message}", client_socket)
        except:
            # If the client's socket is non-blocking and no message is available, continue the loop
            continue

# Define a function to broadcast a message to all connected clients
def broadcast(message, sender_socket):
    for client in clients:
        # Skip the client that sent the message
        if client != sender_socket:
            try:
                # Send the message to the client
                client.send(message.encode())
            except:
                # If the client's socket is closed, remove them from the list of connected clients
                client.close()
                clients.remove(client)

# Define the main function to start the server
def start_server():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the IP address and port number
    server_socket.bind((IP, PORT))

    # Start listening for incoming connections
    server_socket.listen(10)
    print(f"Listening for incoming connections on {IP}:{PORT}")

    # Continuously accept incoming connections
    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()

        # Add the new client to the list of connected clients
        clients.add(client_socket)

        # Create a new thread to handle messages from the client
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

# Define the list of connected clients
clients = set()

# Start the server
start_server()
