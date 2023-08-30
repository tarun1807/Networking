import socket
import os

def handle_client(client_socket):
    current_dir = os.getcwd()

    # Send initial directory to client
    client_socket.sendall(current_dir.encode())
    print(f"Current directory: {current_dir}")
    
    while True:
        # Receive command from client
        command = client_socket.recv(1024).decode('utf-8')

        if not command:
            break

        # Get directory on which command will work
        command_dir = current_dir
        if 'cd ' in command:
            path = command[3:].strip()
            if os.path.isabs(path):
                command_dir = path
            else:
                command_dir = os.path.join(current_dir, path)

        # Execute command and get output
        output = ''
        # try:
        #     if 'cd ' in command:
        #         if 'cd ..' in command:
        #             os.chdir(command_dir)
        #             last_dir_index = command_dir.rfind("\\")
        #             command_dir = command_dir[:last_dir_index]
        #             output = f"Changed directory to {command_dir}\n"
        #             current_dir = command_dir
        #             print(current_dir)
        #         else :
        #             os.chdir(command_dir)
        #             output = f"Changed directory to {command_dir}\n"
        #             current_dir = command_dir
        #     else:
        #         result = os.popen(command).read()
        #         output = f"{result}\n"
        # except Exception as e:
        #     output = f"Error: {str(e)}\n"


        try:
            if 'cd ' in command:
                if command == 'cd ..':
                    # If the command is "cd ..", remove the last directory from the path
                    last_dir_index = command_dir.rfind("\\")
                    second_last_dir_index = command_dir.rfind("\\", 0, last_dir_index)
                    command_dir = command_dir[:second_last_dir_index]
                    # print(command_dir)
                    # print(last_dir_index)
                    # command_dir = command_dir[:last_dir_index]
                    # print(command_dir)
                    os.chdir(command_dir)
                    output = f"Changed directory to {command_dir}\n"
                    current_dir = command_dir
                else:
                    os.chdir(command_dir)
                    output = f"Changed directory to {command_dir}\n"
                    current_dir = command_dir
                
            else:
                result = os.popen(command).read()
                output = f"{result}\n"
        except Exception as e:
            output = f"Error: {str(e)}\n"




        # Send output back to client
        client_socket.send(output.encode('utf-8'))
        client_socket.send(current_dir.encode('utf-8'))
        # # Send directory on which command will work and output back to client
        # print("sendiiing")
        # client_socket.sendall(f"{current_dir}> {output}".encode('utf-8'))
        # print("sendt")
    client_socket.close()

def main():
    host = '127.0.0.1'
    port = 9999

    # Create socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")

    while True:
        # Wait for a connection
        client_socket, address = server_socket.accept()
        print(f"Connected to {address[0]}:{address[1]}")

        # Handle client requests
        handle_client(client_socket)

if __name__ == '__main__':
    main()
