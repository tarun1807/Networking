import socket
import packet_generator
import base64
import sys
import os
import json
import getpass
import packet_reverse

class client:
    def __init__(self):
        self.port = 9999
        self.port2 = 9998
        self.client_name = socket.gethostname()
        self.packets = []
        print(f"{self.client_name} starting as client")

    def create_socket(self):
        try:
            self.s = socket.socket()
            print("Socket created successfully")
        except socket.error as msg:
            print(f"Socket Creation Error: {msg}")
    
    def bind_socket(self):
        try:
            self.s.bind(("", self.port2))
            self.s.listen(5)
            print("Socket Binded successfully, listening to clients")
        except socket.error as msg:
            print(f"Socket Binding Error: {msg}")


    def connect(self):
        self.server_address = input("Enter server's address you want to connect: ")

        self.s.connect((self.server_address, self.port))
        print("Connection established, ready to send and receive messages")
        self.receive_server_name()
        
        self.username = input("username: ")
        self.passwd = getpass.getpass("password: ")

        self.s.send(str.encode(f"{self.username}|{self.passwd}"))

        token = self.s.recv(1024).decode()
        if token != "Certificate Verified!":
            print("You are not registered with the entered username and password, would be done!")
        
        self.send(self.s)
        
        
    def receive_server_name(self):
        self.server_name = self.s.recv(1024).decode("UTF-8")
        print(f"Connection established to {self.server_name}")
        self.send_name()

    def send_name(self):
        self.s.send(str.encode(self.client_name))

    def send_name2(self, conn):
        conn.send(str.encode(self.client_name))
        
    def send(self, conn):
        while True:
            msg = input("Press\n 1. send\n 2. receive\n 3. quit\n ")
            if msg.lower() == "1":
                self.address = input("Enter destination address: ")
                self.s.send(str.encode(self.address))

                print("What type of File/Message you want to send?")
                print("1. Text Message\n2. Text File\n3. Image File")
                ch = input("")
                if ch == "1":
                    self.send_string(conn)
                if ch == "2":
                    self.send_txt(conn)
                if ch == "3":
                    self.send_image(conn)
                if ch == '4':
                    self.send_audio(self.conn)
            
            elif msg.lower() == "2":
                
                self.create_socket()
                self.bind_socket()
                self.accept_socket()

            else:                
                conn.close()
                self.s.close()
                sys.exit()

    def accept_socket(self):
        self.conn, self.address = self.s.accept()
        self.s.setblocking(1)
        self.send_name2(self.conn)
        self.client_name = self.conn.recv(1024).decode("UTF-8")
        print(f"Connection established:\nName: {self.client_name}\tIP:{self.address[0]}\tPORT:{self.address[1]}")  
        self.receive_data()
        self.conn.close()

    def receive_data(self):
        while True:
            try:
                self.type = self.conn.recv(1024).decode("UTF-8")
                if not self.type:
                    print("Connection broken from server's side")
                    self.conn.close()
                    sys.exit()

                print(f"Message received: {self.type}")
                
                if self.type == "Sending a string message":
                    self.conn.send(str.encode("TEMP"))
                    self.receive_string()
                elif self.type == "Sending a txt file":
                    self.receive_txt()
                elif self.type == "Sending an image file":
                    self.receive_image()
                else:
                    self.receive_audio()

            except socket.error as msg:
                print(f"Error while receiving data {msg}")

            except Exception as e:
                print("Connection broken forcefully.", e)
                break
    
    def receive_string(self):
        self.msg = ""
        while True:
            try:
                self.data = self.conn.recv(1024).decode("UTF-8")
                pkt = packet_reverse.packet()
                msg, pkt_id, pkt_num = pkt.convert(self.data)

                print(f"Packet Received: ", pkt_id+1)
                self.msg += msg

                
                self.conn.send(str.encode(f"Packet Received: {pkt_id+1}" ))

                if pkt_id+1 == pkt_num:
                    print(f"Message received: {self.msg}")
                    break

            except socket.error as msg:
                print(f"Error while receiving data {msg}")

            except:
                print("Connection broken forcefully.")
                break

    def receive_txt(self):
        self.msg = ""
        self.conn.send(str.encode("temp"))
        self.file_name = self.conn.recv(1024).decode("UTF-8")
        print("Filename", self.file_name)
        self.conn.send(str.encode("temp2"))
        
        while True:
            try:
                self.data = self.conn.recv(1024).decode("UTF-8")
                
                pkt = packet_reverse.packet()
                msg, pkt_id, pkt_num = pkt.convert(self.data)
                print(f"Packet Received: ", pkt_id+1)
                self.msg += msg

                
                self.conn.send(str.encode(f"Packet Received: {pkt_id+1}" ))

                if pkt_id+1 == pkt_num:
                    print(f"Message received: {self.msg}")
                    file = open(f"{self.file_name}", 'w')
                    file.write(self.msg)
                    file.close()
                    break

            except socket.error as msg:
                print(f"Error while receiving data {msg}")

            except Exception as e:
                print("Connection broken forcefully.", e)
                break
    
    def receive_image(self):
        self.msg = ""
        self.conn.send(str.encode("temp"))
        self.file_name = self.conn.recv(1024).decode("UTF-8")
        print("Filename", self.file_name)
        self.conn.send(str.encode("temp2"))
        
        while True:
            try:
                self.data = self.conn.recv(2000).decode("UTF-8")
                pkt = packet_reverse.packet()
                msg, pkt_id, pkt_num = pkt.convert(self.data)
                print(f"Packet Received: ", pkt_id+1)
                self.msg += msg

                
                self.conn.send(str.encode(f"Packet Received: {pkt_id+1}" ))

                if pkt_id+1 == pkt_num:
                    print(f"Image received")
                    
                    self.msg = self.msg[2:-1]
                    
                    file = open(f"{self.file_name}", 'wb')
                    file.write(base64.b64decode(self.msg))
                    file.close()

                    break

            except socket.error as msg:
                print(f"Error while receiving data {msg}")

            except Exception as e:
                print("Connection broken forcefully.", e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

                break

    def receive_audio(self):
        pass
    

    def send_string(self, conn):
        msg = input("Enter what you want to send: ")
        payload = int(input("Enter size of payload: "))

        pkt = packet_generator.packet_convert(msg, payload, self.server_name, self.server_address, self.client_name, self.address, self.username, self.passwd, "string")
        packets = pkt.convert_to_packet()
        for packet in packets:
            
            conn.send(str.encode(json.dumps(packet)))
            msg = conn.recv(1024).decode("UTF-8")
            
            print(msg)

    def send_txt(self, conn):
        location = input("Enter location: ")
        payload = int(input("Enter size of payload: "))

        file = open(location, 'r')
        msg = file.readlines()[0]
        filename = input("Enter file name with its extension: ")

        pkt = packet_generator.packet_convert(msg, payload, self.server_name, self.server_address, self.client_name, self.address, self.username, self.passwd, f"text|{filename}")
        
        
        packets = pkt.convert_to_packet()
        for packet in packets:
            packet['Filename'] = location
            
            conn.send(str.encode(json.dumps(packet)))
            msg = conn.recv(1024).decode("UTF-8")
            
            print(msg)

    def send_image(self, conn):
        location = input("Enter location: ")
        payload = int(input("Enter size of payload: "))
        name = input("Enter file name: ")
        
        with open(location, "rb") as image:
            msg = str(base64.b64encode(image.read()))
        
        pkt = packet_generator.packet_convert(msg, payload, self.server_name, self.server_address, self.client_name, self.address, self.username, self.passwd, f"image|{name}")
        
        packets = pkt.convert_to_packet()
        for packet in packets:
            packet['Filename'] = location
            
            conn.send(str.encode(json.dumps(packet)))
            msg = conn.recv(1024).decode("UTF-8")
            
            print(msg)


    
cl = client()
cl.create_socket()
cl.connect()
