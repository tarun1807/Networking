
import socket
from threading import Thread
import defense
import json
from collections import defaultdict

class Server:
    def __init__(self):
        self.buffer = defaultdict(list)
        self.port = 9999

    def start(self):
        self.server_name = socket.gethostname()
        server = socket.socket()

        server.bind(("", self.port))
        print(f"{self.server_name} starting as server")
        server.listen(5)

        receive_thread = receive(server, self.buffer)
        receive_thread.start()

        send_thread = send(self.buffer)
        send_thread.start()
        


class receive(Thread):
    def __init__(self, server_socket, buffer):
        super().__init__()
        self.server_socket = server_socket
        self.buffer = buffer
        self.client_name = socket.gethostname()
    
        self.sc = defense.certificate()
        
    def run(self):
        while True:
            print("Trying to connect")
            client_socket, client_add = self.server_socket.accept()
            self.server_socket.setblocking(1)

            self.send_name(client_socket)
            self.client_name = client_socket.recv(1024).decode("UTF-8")
            print(f"Connected established\nName: {self.client_name} IP: {client_add[0]}| PORT: {client_add[1]}")
            
            user, passwd = client_socket.recv(1024).decode().split('|')
            
            if self.sc.verify(user, passwd) != "Certificate Verified successfully!":
                self.sc.add(user, passwd)
                client_socket.send(str.encode("Certificate not verified!"))
            else:
                client_socket.send(str.encode("Certificate Verified!"))

            flag = 1 

            packets = []
            
            while True:
                if flag == 1:
                    receiver_ip = client_socket.recv(1024).decode()
                    flag = 0

                packet = client_socket.recv(2000).decode('UTF-8')
                
                if not packet:
                    print(f"{client_add[0]} just disconnected!")
                    break

                client_socket.send(str.encode(f"Packet Received: {(len(packets))}" ))
                temp = json.loads(packet)
                
                if self.sc.verify(temp['Certificate']['Username'], temp['Certificate']['Password']) == "Certificate Verified successfully!":
                    packets.append([packet])

                    print("Packet added to buffer")
                    if temp["Packet ID"] == temp["Number of Packets"]-1:
                        self.buffer[receiver_ip].append(packets)
                        print(self.buffer)
                        packets = []
                        flag = 1
                        

                
            client_socket.send(str.encode("OK"))

            
            client_socket.close()
            
    def send_name(self, client_socket):
        client_socket.send(str.encode(self.client_name))
 
    
class send(Thread):
    def __init__(self, buffer):
        super().__init__()
        self.buffer = buffer
        self.client_name = socket.gethostname()
    
    def receive_server_name(self, socket):
        self.server_name = socket.recv(1024).decode("UTF-8")
        print(f"Connection established to {self.server_name}")
        self.send_name(socket)

    def send_name(self, socket):
        socket.send(str.encode(self.client_name))

    def run(self):
        while True:
            
            if self.buffer:
                print("Trying to send packet")

                ips = list(self.buffer.keys())
                for ip in ips:

                    try:
                        desti_socket = socket.socket()
                        desti_socket.connect((ip, 9998))
                        self.receive_server_name(desti_socket)
                        flag = 1
                        while self.buffer[ip]:
                            for complete in self.buffer[ip]:
                                for packet in complete:
                                    data = packet.pop(0)
                                    tempm = json.loads(data)
                                    type_msg = tempm['Type']
                                    
                                    if flag == 1:
                                        if  type_msg == "string":
                                            desti_socket.send(str.encode("Sending a string message"))
                                            temp = desti_socket.recv(1024).decode("UTF-8")
                            
                                            flag = 0
                                            
                                        elif "text" in type_msg:
                                            desti_socket.send(str.encode("Sending a txt file"))
                                            
                                            flag = 0
                                            temp = desti_socket.recv(1024).decode("UTF-8")
                            
                                            desti_socket.send(str.encode(type_msg.split('|')[1]))
                                            temp2 = desti_socket.recv(1024).decode("UTF-8")
                                        else:
                                            desti_socket.send(str.encode("Sending an image file"))
                                            flag = 0
                                            temp = desti_socket.recv(1024).decode("UTF-8")
                            
                                            desti_socket.send(str.encode(type_msg.split('|')[1]))
                                            temp2 = desti_socket.recv(1024).decode("UTF-8")
                                    
                                    if tempm['Packet ID'] == tempm["Number of Packets"]-1:
                                        self.buffer[ip] = []
                                        flag = 1
                                    
                                    if "image" in tempm['Type']:
                                        desti_socket.send(str.encode(data)) 
                                    else:
                                        desti_socket.send(str.encode(data))
                                    
                                    ack = desti_socket.recv(1024).decode("UTF-8")
                                    
                                    if ack:
                                        print("Packet sent successfully")
                                    else:
                                        self.buffer[ip].append([data])
                            del self.buffer[ip]
                        desti_socket.close()
                        del self.buffer[ip]

                    except Exception as e:
                        pass
                        # print(e)
                        # exc_type, exc_obj, exc_tb = sys.exc_info()
                        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        # print(exc_type, fname, exc_tb.tb_lineno)
            else:
                print("Empty buffer")
                

server = Server()
server.start()