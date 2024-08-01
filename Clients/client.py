import socket 
import argparse

def join_action(sock, host, port):
    try:
    # Connecting with Server 
        sock.connect((host, int(port))) 
        print("Connection to the File Exchange Server is successful!")
    
    except (socket.error, ValueError) as e:
        print("Error: Connection to the Server has failed! Please check IP Address and Port Number.")
   


def leave_action(sock):
    sock.close()
    print("Connection closed. Thank you!")

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

    except IOError: 
        print('Error: File not found.') 

def dir(sock):
    # Send a request to the server to list the directory
    request = "LIST_DIR"
    sock.sendall(request.encode())

    # Receive the response from the server
    # Assume the server sends a single string with file names separated by newline characters
    response = sock.recv(4096).decode()

    # Print the received list of files
    print("Files in the server directory:")
    print(response)
    print("Dir command executed!")

def register_action(sock, alias):
    # Send a request to the server to list the directory
    request = f"REGISTER_ALIAS {alias}"
    sock.sendall(request.encode())

    # Receive the response from the server
    # Assume the server sends a single string with file names separated by newline characters
    response = sock.recv(4096).decode()
    print(response)



# Creating Client Socket 
if __name__ == '__main__': 

    # host = '127.0.0.1'
    # port = 8080
    userHandle = "ClientX"
  
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
            try:
            register_action(sock, clientinput[1])
            except Exception as e:
                print("Error: Command parameters do not match or is not allowed.")
        elif command == '/store':
            storeFile(clientinput[1])

        elif command == '/dir':
            dir(sock)

        elif command == '/?':
            print("Available commands:\n/join <server_ip_add> <port> - Connects to the server application\n/leave - Disconnects from the server application\n/register <handle> - Registers a unique handle or alias\n/store <filename> - Send file to server\n/dir - Request directory file list from a server\n/get <filename> - Fetches a file from a server\n/? - Shows this help message")
        else:
            print("Error: Command not found.")

