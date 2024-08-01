import socket 
import os

# def handle_client(conn):
#         # Receive request from the client
#         request = conn.recv(1024).decode()
#         if request == "LIST_DIR":
#             # Get the list of files in the current directory
#             files = os.listdir(".")
#             # Join the list into a single string, separated by newlines
#             response = "\n".join(files)
#             # Send the response back to the client
#             conn.sendall(response.encode())
#             # Add additional command handling as needed
  
if __name__ == '__main__': 
    # Defining Socket 
    host = '127.0.0.1'
    port = 8080
    totalclient = 1
    
    # int(input('Enter number of clients: ')) 
  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.bind((host, port)) 
    sock.listen(totalclient) 
    # Establishing Connections 
    connections = [] 
    client_list = {}
    print('Initiating clients') 
    for i in range(totalclient): 
        conn = sock.accept() 
        connections.append(conn)
        print('Connected with client', i+1)


        client_list[conn] = {
            'socket': conn,
            'alias': ""
        }
  
    fileno = 0
    idx = 0
    for conn in connections: 
        # Receiving File Data 
        idx += 1
        print(conn)
        
        data = conn[0].recv(1024).decode() 
        if data == "LIST_DIR":
            print('Getting directory')
            files = [f for f in os.listdir(".") if f.endswith(".txt")]
            response = "\n".join(files)
            conn[0].send(response.encode())

        elif data.startswith("REGISTER_ALIAS"):
            _, alias = data.split(maxsplit=1)  # Extract alias
            client_info = client_list.get(client_socket)
            if client_info:
                client_info['alias'] = alias  # Update alias
                response = f"Alias registered as {alias}"
                client_socket.send(response.encode())


        if not data: 
            continue
    # Creating a new file at server end and writing the data 
        filename = 'output'+str(fileno)+'.txt'
        fileno = fileno+1
        fo = open(filename, "w") 
        while data: 
            if not data: 
                break
            else: 
                fo.write(data) 
                data = conn[0].recv(1024).decode() 

        print() 
        print('Receiving file from client', idx) 
        print() 
        print('Received successfully! New filename is:', filename)


        fo.close() 
    # Closing all Connections 
    for conn in connections: 
        conn[0].close() 

