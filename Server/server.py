import socket
import threading
import os
import datetime

# Initialize client_list as a dictionary
client_list = {}

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(4096).decode()
            if not data:
                break

            if data.startswith("REGISTER_ALIAS"):
                _, alias = data.split(maxsplit=1)  # Extract alias

                alias_exists = any(client['alias'] == alias for client in client_list.values())
                if alias_exists:
                    response = "Error: Registration failed. Handle or alias already exists."
                    client_socket.send(response.encode())
                else:     
                # Update the alias for this client
                    if client_socket in client_list:
                        client_list[client_socket]['alias'] = alias
                        response = f"Welcome {alias}!"
                        client_socket.send(response.encode())
                    else:
                        response = "Error: Client not found"
                        client_socket.send(response.encode())

            elif data == "LIST_DIR":
                print('Getting directory')
                files = [f for f in os.listdir(".") if f.endswith(".txt")]
                response = "\n".join(files)
                client_socket.send(response.encode())

            elif data.startswith("STORE_FILE"):
                
                alias = client_list[client_socket]['alias']
            
                _, file_data = data.split(' ', 1)  # Split to remove command
            
            # Split the data into file name and contents
                if '\n' in file_data:
                    file_name, file_contents = file_data.split('\n', 1)  # Split into file name and contents
                    # Save the file
                    with open(file_name, "w") as file:
                        file.write(file_contents)
                    
                    print(f"Received file: {file_name}")
                    formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    response = f"{alias}<{formatted_time}>: Uploaded {file_name}"
                    client_socket.send(response.encode())

            elif data.startswith("GET_FILE"):
                
                _, file_name = data.split(maxsplit=1)  # Extract file name
                try:
                    # Reading file and sending data to client

                    file = open(file_name, "r") 
                    data = file.read()
                    if not data:
                        print("Nothing here.")
                    # while data: 
                            # sock.send(str(data).encode()) 
                            # data = file.read() 
                        # File is closed after data is sent 
                    file.close()
                    request = f"{file_name}\n{data}"
                    client_socket.sendall(request.encode())
                    response = client_socket.recv(4096).decode()

                    print(response)
                
                except IOError: 
                    response = "Error: File not found in the server."
                    client_socket.sendall(response.encode())
                    print('Error: File not found in the server.')

            
            else:
                    print(f"Unknown command: {data}")

    finally:
        # Remove the client from the dictionary on disconnection
        if client_socket in client_list:
            alias = client_list[client_socket]['alias']
            del client_list[client_socket]
            client_socket.close()
            
            if(alias != ""):
                print(f"{alias} disconnected.")
            else:
                print("Client disconnected.")
                
def main():
    host = '127.0.0.1'
    port = 8080
    total_clients = 4

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