#IMPORTING LIBRARIES
import socket
from threading import Thread
import json
import os
import sys
import time
from collections import defaultdict
from prettytable import PrettyTable

#SERVER CLASS
class Server:
    def __init__(self):
        self.ping_requests = defaultdict(dict)
        self.port = 9999
        self.routing_table = defaultdict(dict)

#DECLARING A SOCKET TO CONNECT TO SERVER WHILE RECEIVING PING
    def start(self):
        self.server_name = socket.gethostname()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(1)

        server.bind(("", self.port))
        print(f"{self.server_name} starting as server")
        server.listen(5)

#STARTING RECEIVING PING THREAD
        receive_thread = receive(server, self.ping_requests, self.routing_table)
        receive_thread.start()

#STARTING SEND PING THREAD
        send_thread = send(self.ping_requests, self.routing_table)
        send_thread.start()
        

#RECEIVE CLASS
class receive(Thread):
    def __init__(self, server_socket, requests, routing_table) :
        super().__init__()

        self.server_socket = server_socket

        self.ping_requests = requests
        self.routing_table = routing_table
        self.server_name = socket.gethostname()

    def run(self):

        while True:

#ACCEPT THE SERVER'S REQUEST TO RECEIVE PING
            print(f"Ready to connect to {len(self.routing_table)+1} device: ")

            client_socket, client_add = self.server_socket.accept()
            client_thread = Thread(target = self.receive_request, args = (client_socket, client_add))
            
            client_name = client_socket.recv(1024).decode("UTF-8")
            self.routing_table[client_add[0]] = {"Socket" : client_socket, "Name" : client_name,"Port ID" : client_add[1], "Received Flag" : 0, "Time Message" : ""}
            
            
            client_socket.send(str.encode("TEMP")) 
            client_thread.start()

#PRINT ROUTING TABLE
    def print_routing(self, routing_table):
        header = ['S. No.', 'Machine Name', 'IP Address', 'Port Number']
        
        table = PrettyTable(field_names=header, align='l')
        for ind, ip in enumerate(routing_table):
            table.add_row([ind+1, routing_table[ip]['Name'],ip, routing_table[ip]['Port ID']])
        
        print(table, "\n")

#RECEIVE PING REQUESTS FROM A CLIENT CONNECTED THROUGH A THREAD
    def receive_request(self, sock, client_add):
        flag = 1
        try:
            while True and flag == 1:
                temp = sock.recv(1024).decode("UTF-8")
                
                if len(temp) == 0:
                    continue
                
                client_name, receiver_client = temp.split(" ")
                
                self.print_routing(self.routing_table)
                
                #IF RECEIVER IS NOT IN ROUTING TABLE, WE CONVEY WE COULDN'T PING TO SENDER
                if receiver_client not in self.routing_table:
                    sock.send(str.encode("not pinged"))
                    continue

                else:
                    sock.send(str.encode(f"can be pinged|{self.server_name}"))

                while True:
                    
                    #RECEIVE PING REQUEST
                    ping = sock.recv(1024).decode("UTF-8")
                    ping = json.loads(ping)
                    
                    self.ping_requests[receiver_client] = ping

                    sock.send(str.encode("TEMP"))

                    task = sock.recv(1024).decode("UTF-8")
                    
                    #IF PING IS RECEIVED, CHANGE FLAG OF RECEIVED AND SEND MESSAGE TO SENDER
                    if task == "FINISHED":
                        while self.routing_table[client_add[0]]['Received Flag'] != 1:
                            pass
                        
                        data = f"RECEIVED|{self.routing_table[client_add[0]]['Time Message']}"
                        sock.send(str.encode(data))
                        self.routing_table[client_add[0]]['Received Flag'] = 0
                        self.routing_table[client_add[0]]['Time Message'] = ""
                        
                        continuation = sock.recv(1024).decode("UTF-8")

                    #IF STILL CLIENT RECEIVE REQUEST TO SEND PING    
                        if continuation == "y":
                            break
                        else:
                            sock.close()
                            del self.routing_table[client_add[0]]
                            flag = 0
                            break

                if flag == 0:
                    break

        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

#SEND CLASS
class send(Thread):
    def __init__(self, requests, routing_table) :
        super().__init__()

        self.ping_requests = requests
        self.routing_table = routing_table

    def run(self):
        while True:
            try:
                flag = 1

                while True and flag == 1:
                    if self.ping_requests:

                        #SERVER TRIES TO PING RECEIVER
                        print("Trying to send ping")
                        
                        for ip in self.ping_requests.copy():
                            try:

                                #SERVER TRIES TO CONNECT WITH SERVER
                                client2 = socket.socket()
                                client2.connect((ip, 9998))

                                print(f"Connected to IP: {client2.getpeername()[0]}| Port ID: {client2.getpeername()[1]}")
                                
                                #IF RECEIVER IS IN ROUTING TABLE, TRY TO PING
                                while self.ping_requests[ip]:
                                    ping_ip = self.ping_requests[ip]["Sender"]
                                    times = self.ping_requests[ip]["Times"]

                                    str_time = ""

                                    #PING FOR N TIMES SPECIFIED BY SENDER
                                    for i in range(times):
                                        start = time.time()
                                        client2.send(str.encode(f"Ping {i+1} out of {times} sent by {ping_ip}"))
                                        temp = client2.recv(1024).decode("UTF-8")
                                        end = time.time()
                                        str_time += f"Reply from {ip}: {(end-start)*1000}\n"

                                    #AFTER SENDING PING, SEND A FINISHED ACKNOWLDGEMENT TO SENDER
                                    client2.send(str.encode("FINISHED"))
                                    ack = client2.recv(1024).decode("UTF-8")
                                    
                                    if ack == "DONE":
                                        del self.ping_requests[ip]
                                        flag = 0

                                        #CHANGE FLAG STATUS TO YES, TO SEND PING
                                        self.routing_table[ping_ip]['Received Flag'] = 1
                                        self.routing_table[ping_ip]['Time Message'] = str_time
                                        
                                        break
                                

                            except Exception as e:
                                print(e)
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                print(exc_type, fname, exc_tb.tb_lineno)

                    else:
                        pass

            except Exception as e:
                print(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

#SERVER OBJECT
server = Server()
server.start()