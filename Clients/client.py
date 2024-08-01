import socket 
import argparse

connected = 0
registered = 0

def join_action(sock, host, port):
    global connected
    try:
    # Connecting with Server 
        sock.connect((host, int(port))) 
        connected = 1
        print("Connection to the File Exchange Server is successful!")

    except (socket.error, ValueError) as e:
        print("Error: Connection to the Server has failed! Please check IP Address and Port Number.")
    


def leave_action(sock):
    try:
        global connected
        global registered
        connected = 0
        registered = 0
        sock.close()
        print("Connection closed. Thank you!")
    except (ConnectionResetError, ConnectionRefusedError, BrokenPipeError) as e:
        print("Error: Connection to the Server Lost.")

def storeFile(fileName):
    try: 
    # Reading file and sending data to server 

        file = open(fileName, "r") 
        data = file.read()
        if not data:
            print("Nothing here.")
        # while data: 
                # sock.send(str(data).encode()) 
                # data = file.read() 
            # File is closed after data is sent 
        file.close()
        request = f"STORE_FILE {fileName}\n{data}"
        sock.sendall(request.encode())
        response = sock.recv(4096).decode()

        print(response)
    except (ConnectionResetError, ConnectionRefusedError, BrokenPipeError) as e:
        print("Error: Connection to the Server Lost.")
    except IOError: 
        print('Error: File not found.') 

def dir(sock):
    try: 
        # Send a request to the server to list the directory
        request = "LIST_DIR"
        sock.sendall(request.encode())

        # Receive the response from the server
        # Assume the server sends a single string with file names separated by newline characters
        response = sock.recv(4096).decode()

        # Print the received list of files
        print("Server Directory")
        print(response)
    except (ConnectionResetError, ConnectionRefusedError, BrokenPipeError) as e:
        print("Error: Connection to the Server Lost.")

def register_action(sock, alias):
    try:
        global registered
        # Send a request to the server to list the directory
        request = f"REGISTER_ALIAS {alias}"
        sock.sendall(request.encode())

        # Receive the response from the server
        # Assume the server sends a single string with file names separated by newline characters
        response = sock.recv(4096).decode()
        registered = 1
        print(response)
    except (ConnectionResetError, ConnectionRefusedError, BrokenPipeError) as e:
        print("Error: Connection to the Server Lost.")


def getFile(sock, fileName):
    try:
        # Send a request to the server to get the file
        request = f"GET_FILE {fileName}"
        sock.sendall(request.encode())

        # Receive the response from the server
        # Assume the server sends a single string with file names separated by newline characters
        response = sock.recv(4096).decode()
                
        # Split the data into file name and contents
        if '\n' in response:
            file_name, file_contents = response.split('\n', 1)  # Split into file name and contents
            # Save the file
            with open(file_name, "w") as file:
                file.write(file_contents)

            print(f"File received from Server: {file_name}")
            # formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # response = f"{alias}<{formatted_time}>: Uploaded {file_name}"
            response = f"Uploaded file: {file_name}"
            sock.send(response.encode())

        else:
            print(response)
    except (ConnectionResetError, ConnectionRefusedError, BrokenPipeError) as e:
        print("Error: Connection to the Server Lost.")



# Creating Client Socket 
if __name__ == '__main__': 

    # host = '127.0.0.1'
    # port = 8080
  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    while True: 
        
        clientinput = input("").strip().split()
        command = clientinput[0]

        if command == '/join':
            try:
                join_action(sock, clientinput[1], clientinput[2])
            except Exception as e:
                print("Error: Command parameters do not match or is not allowed.")

        elif command == '/leave':
            try:
                sock.send(b'')
                leave_action(sock)
            except Exception as e:
                print("Error: Disconnection failed. Please connect to the server first.")

        elif command == '/register':
            
            if (connected == 1):
                try:
                    register_action(sock, clientinput[1])
                except Exception as e:
                    print("Error: Command parameters do not match or is not allowed.")
            else:
                print("Error: Registration Failed. Please connect to the server first.")

        elif command == '/store':
            if (connected == 1 and registered == 1):
                try:
                    storeFile(clientinput[1])
                except Exception as e:
                    print("Error: Command parameters do not match or is not allowed.")
            elif (connected == 1 and registered == 0):
                print("Error: Store Request failed. Please register first.")
            else:
                print("Error: Store Request failed. Please connect to the server first.")

        elif command == '/dir':
            if (connected == 1 and registered == 1):
                dir(sock)
            elif (connected == 1 and registered == 0):
                print("Error: Directory Request failed. Please register first.")
            else:
                print("Error: Directory Request failed. Please connect to the server first.")
                
        elif command == '/get':
            if (connected == 1 and registered == 1):
                try:
                    getFile(sock, clientinput[1])
                except Exception as e:
                    print("Error: Command parameters do not match or is not allowed.")
            elif (connected == 1 and registered == 0):
                print("Error: Get Request failed. Please register first.")
            else:
                print("Error: Get Request Failed. Please connect to the server first.")
                
        elif command == '/?':
            print("Available commands:\n/join <server_ip_add> <port> - Connects to the server application\n/leave - Disconnects from the server application\n/register <handle> - Registers a unique handle or alias\n/store <filename> - Send file to server\n/dir - Request directory file list from a server\n/get <filename> - Fetches a file from a server\n/? - Shows this help message")

        else:
            print("Error: Command not found.")

