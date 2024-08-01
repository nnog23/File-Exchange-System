import socket 
import argparse

def join_action(sock, host, port):

    # Connecting with Server 
    sock.connect((host, int(port))) 
    print("Join command executed!")
    
def leave_action(sock):
    sock.close()
    print("Leave command executed!")
def register_action():
    print("Register command executed!")
# Creating Client Socket 
if __name__ == '__main__': 

    # host = '127.0.0.1'
    # port = 8080
  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    while True: 
        
        clientinput = input("").strip().split()
        command = clientinput[0]

        if command == '/join':
            print(command)
            join_action(sock, clientinput[1], clientinput[2])

        elif command == '/leave':
            leave_action(sock)
        elif command == '/register':
            register_action()
        elif command == '/help':
            print("Available commands:\n/join - Executes the join action\n/hello - Executes the hello action\n/exit - Exits the program\n/help - Shows this help message")
        else:
            print("Unknown command. Type /help for a list of available commands.")

'''
        filename = input('Input filename you want to send: ') 
        try: 
           # Reading file and sending data to server 
            fi = open(filename, "r") 
            data = fi.read() 
            if not data: 
                break
            while data: 
                sock.send(str(data).encode()) 
                data = fi.read() 
            # File is closed after data is sent 
            fi.close() 

        except IOError: 
            print('You entered an invalid filename! Please enter a valid name') 
'''