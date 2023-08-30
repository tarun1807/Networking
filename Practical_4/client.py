#IMPORTING LIBRARIES
import socket
from threading import Thread
import json
import os
import time
import sys


#CLIENT CLASS
class Client:
    def __init__(self):
        self.port = 9998
        
    def start(self):
#DECLARING A SOCKET TO CONNECT TO SERVER WHILE RECEIVING PING
        client = socket.socket()
        self.client_name = socket.gethostname()
        
        client.bind(("", self.port))
        print(f"{self.client_name} starting as client")
        client.listen(5)


#STARTING RECEIVING PING THREAD
        receive_thread = receive_ping(client)
        receive_thread.start()

#STARTING SEND PING THREAD
        send_thread = send_ping()
        send_thread.start()
        

#RECEIVE PING CLASS
class receive_ping(Thread):
    def __init__(self, client_socket) :
        super().__init__()
        self.client_socket = client_socket
    
    def run(self):
        while True:
            
            #ACCEPT THE SERVER'S REQUEST TO RECEIVE PING
            server_socket, server_add = self.client_socket.accept()
        
            while True:
                ping = server_socket.recv(1024).decode("UTF-8")

                #IF MESSAGE IS PING, THEN ACKNOWLEDGE IT
                if "Ping" in ping:    
                    server_socket.send(str.encode("received"))

                #IF MESSAGE IS FINISHED, THEN CLOSE THE CONNECTION
                elif ping == "FINISHED":
                    server_socket.send(str.encode("DONE"))
                    server_socket.close()
                    break

#SEND PING CLASS      
class send_ping(Thread):
    def __init__(self) :
        super().__init__()

#ENTER SERVER'S ADDRESS
        self.server_address = input("Enter server's address: ")
        
    
    def run(self):
        try:

#CONNECT TO THE SERVER TO SEND PING REQUEST
            client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#TO STAY CONNECTED UNTIL FORCEFULL BREAKING CONNECTION
            client2.setblocking(1)

            self.client_name = socket.gethostname()
            client2.connect((self.server_address, 9999))
            
            client2.send(str.encode(self.client_name))
            client2.recv(1024) #TEMP

            while True:

#INPUT TO WHOM PERFORM PING
                content = input("Enter ping address [ping ip -times]").split(" ")
                start = time.time()

                self.ping_request = {}

                if len(content) == 2 or len(content) == 3:
                    receiver_ip = content[1]
                else:
                    print("Wrong Syntax")
                    continue

                client2.send(str.encode(f"{self.client_name} {receiver_ip}"))
                server_name = client2.recv(1024).decode("UTF-8")
                
                if len(content) == 2:
                    self.ping_request["Times"] = 1
                    
                elif len(content) == 3:
                    self.ping_request["Times"] = int(content[2])

#IF MACHINE TO BE PINGED IS NOT PRESENT IN ROUTING TABLE OF SERVER, IT SEND NOT PINGED
                if server_name == "not pinged":
                    end = time.time()
                    temp = self.ping_request["Times"]
                    
#PRINT STATISTICS ABOUT THE PING REQUEST
                    print(f"\nPing statistics for {receiver_ip}:")
                    print(f"\t Packets: Sent = {temp}, Received = 0 , Loss = 0 (100% loss)")
                    print("Approximate round trip times in milli-seconds:")
                    
                    print(f"\tMinimum = {(end-start)*1000:.0f}ms, Maximum = {(end-start)*1000:.0f}ms, Average = {(end-start)/temp*1000:.0f}ms")
                    print(f"\nPing Unsuccessfull in {(end-start)*1000:.0f} ms")
                    
                    continue
                else:
                    server_name = server_name.split("|")[1]

                self.ping_request["Sender"] = socket.gethostbyname(self.client_name)

                client2.send(str.encode(json.dumps(self.ping_request)))

                temp = client2.recv(1024).decode("UTF-8")
                if temp == "TEMP":
                    client2.send(str.encode("FINISHED"))
                
                ack = client2.recv(1024000).decode("UTF-8")

#RECEIVE ACKNOWLDGMENT AFTER PING IS RECEIVED                 
                if "RECEIVED" in ack:

                    end = time.time()

                    ping_details = ack.split("|")[1].split("\n")[:-1]
                    maxi, mini, tot = float('-inf'), float('inf'), 0
                    
                    print("")

#PRINT PING DETAILS
                    for ping in ping_details:
                        
                        temp = ping.split(": ")
                        temp1 = float(temp[1])
                        print(f"{temp[0]}: bytes={sys.getsizeof(self.ping_request)} time={temp1:.0f}ms")
                        
                        maxi = max(maxi, temp1)
                        mini = min(mini, temp1)
                        tot += temp1 

                    sent = self.ping_request["Times"] 

#PRINT PING STATISTICS 
                    print(f"Ping statistics for {receiver_ip}:")
                    print(f"\t Packets: Sent = {sent}, Received = {len(ping_details)} , Loss = {sent-len(ping_details)} ({(sent-len(ping_details))/sent*100:.0f}% loss)")
                    print("Approximate round trip times in milli-seconds:")
                    print(f"\tMinimum = {mini:.0f}ms, Maximum = {maxi:.0f}ms, Average = {tot/sent:.0f}ms")

                    print(f"\nPing Completed in {(end-start)*1000:.0f} ms")
                    
                    time.sleep(1)
                    
#ENTER YES TO CONTINUE TO PING ELSE PROGRAM ENDS
                    ch = input("Do you want to continue(yes/no): ")
                    
                    if ch != "yes":
                        client2.send(str.encode("n"))
                        client2.close()
                        os._exit(1)
                        
                    else:
                        client2.send(str.encode("y"))

        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

                

client = Client()
client.start()