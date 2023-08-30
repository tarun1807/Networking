import socket

def main():
    cid = input("Enter Client ID: ")
    cip = input("Enter Client IP: ")

    host = input("Enter IP of device you want to access:")

    # host = '127.0.0.1'
    port = 9999

    # Create socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    client_socket.connect((host, port))
    k=0

    while True:
        # Take user input
        # print(k)
        cwd = client_socket.recv(1024).decode()
        k+=1
        # print(k)
        # print(f"{cwd}> ", end="")

        # command = input("Enter a command: ")
        command = input(f"{cwd} >")

        # Send command to server
        client_socket.send(command.encode('utf-8'))

        # Receive output from server
        output = client_socket.recv(1024).decode('utf-8')

        # Display output
        print(output)

        # Break out of loop if exit command entered
        if command == 'exit':
            break

    client_socket.close()

if __name__ == '__main__':
    main()
