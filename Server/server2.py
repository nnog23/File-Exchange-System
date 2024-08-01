import socket
import threading
import os

# Initialize client_list as a dictionary
client_list = {}

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            if data.startswith("REGISTER_ALIAS"):
                _, alias = data.split(maxsplit=1)  # Extract alias
                # Update the alias for this client
                if client_socket in client_list:
                    client_list[client_socket]['alias'] = alias
                    response = f"Alias registered as {alias}"
                    client_socket.send(response.encode())
                    print(client_list)
                else:
                    response = "Error: Client not found"
                    client_socket.send(response.encode())

            elif data == "LIST_DIR":
                print('Getting directory')
                files = [f for f in os.listdir(".") if f.endswith(".txt")]
                response = "\n".join(files)
                client_socket.send(response.encode())

            elif data == "STORE_FILE":
                client_list[client_socket]['alias']
            else:
                print(f"Unknown command: {data}")

    finally:
        # Remove the client from the dictionary on disconnection
        if client_socket in client_list:
            del client_list[client_socket]
        client_socket.close()
        print(f"Client disconnected.")

def main():
    host = '127.0.0.1'
    port = 8080
    total_clients = 3

    # Creating Server Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(total_clients)
    print(f"Server listening on {host}:{port}")

    for i in range(total_clients):
        conn, addr = sock.accept()
        print('Connected with client', i+1)

        # Initialize client information in the dictionary
        client_list[conn] = {
            'socket': conn,
            'alias': ""  # Initial alias is empty
        }

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()

    # Cleanup
    for client_socket in client_list.keys():
        client_socket.close()
    sock.close()

if __name__ == '__main__':
    main()