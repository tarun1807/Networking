import socket
from threading import Thread
import security
import json
from collections import defaultdict
import threading

import random
lock = threading.Lock()

# def alter_packet(packet):
#     # Choose random number of bits to alter
#     num_bits = random.randint(1, len(packet))

#     # Choose random positions to alter bits
#     positions = random.sample(range(len(packet)), num_bits)

#     # Flip the bits at the chosen positions
#     new_packet = bytearray(packet, 'utf-8')
#     for pos in positions:
#         new_packet[pos] = new_packet[pos] ^ 1

#     return bytes(new_packet)

def hammingDist(str1, str2):
    i = 0
    count = 0
 
    while(i < len(str1)):
        if(str1[i] != str2[i]):
            count += 1
        i += 1
    return count

import random

# def alter_packet(packet):
#     if isinstance(packet, dict):
#         new_packet = {}
#         for key, value in packet.items():
#             if key == "Message":
#                 # alter the message by flipping one random bit
#                 binary_message = ''.join(format(ord(char), '08b') for char in value)
#                 bit_to_flip = random.randint(0, len(binary_message)-1)
#                 flipped_bit = '1' if binary_message[bit_to_flip] == '0' else '0'
#                 new_binary_message = binary_message[:bit_to_flip] + flipped_bit + binary_message[bit_to_flip+1:]
#                 new_message = ''.join(chr(int(new_binary_message[i:i+8], 2)) for i in range(0, len(new_binary_message), 8))
#                 new_packet[key] = new_message
#             elif isinstance(value, dict):
#                 new_packet[key] = alter_packet(value)
#             else:
#                 new_packet[key] = value
#         return new_packet
#     else:
#         return packet



# def alter_packet(packet):
#     if isinstance(packet, dict):
#         new_packet = {}
#         for key, value in packet.items():
#             if key == "Message":
#                 # alter the message by flipping one random bit
#                 binary_message = ''.join(format(ord(char), '08b') for char in value)
#                 k = random.randint(2, len(binary_message))
#                 for j in range(k):
#                     bit_to_flip = random.randint(0, len(binary_message)-1)
#                     flipped_bit = '1' if binary_message[bit_to_flip] == '0' else '0'
#                     new_binary_message = binary_message[:bit_to_flip] + flipped_bit + binary_message[bit_to_flip+1:]
#                     new_message = ''.join(chr(int(new_binary_message[i:i+8], 2)) for i in range(0, len(new_binary_message), 8))
#                     new_packet[key] = new_message
#             elif isinstance(value, dict):
#                 new_packet[key] = alter_packet(value)
#             else:
#                 new_packet[key] = value
#         return new_packet
#     else:
#         return packet      new


import random

def alter_packet(packet):
    if isinstance(packet, dict):
        new_packet = {}
        for key, value in packet.items():
            if key == "Message":
                # alter the message by flipping k random bits
                binary_message = ''.join(format(ord(char), '08b') for char in value)
                k = random.randint(2, len(binary_message))
                flipped_indices = set(random.sample(range(len(binary_message)), k))
                new_binary_message = ""
                for i in range(len(binary_message)):
                    if i in flipped_indices:
                        new_binary_message += '1' if binary_message[i] == '0' else '0'
                    else:
                        new_binary_message += binary_message[i]
                new_message = ''.join(chr(int(new_binary_message[i:i+8], 2)) for i in range(0, len(new_binary_message), 8))
                new_packet[key] = new_message
            elif isinstance(value, dict):
                new_packet[key] = alter_packet(value)
            else:
                new_packet[key] = value
        return new_packet
    else:
        return packet



# def alter_packet(packet):
#     if isinstance(packet, dict):
#         new_packet = {}
#         for key, value in packet.items():
#             if key == "Message":
#                 # alter the message by flipping k different random bits, where k is between 1 and the length of the message
#                 binary_message = ''.join(format(ord(char), '08b') for char in value)
#                 k = random.randint(1, len(binary_message))
#                 bits_to_flip = random.sample(range(len(binary_message)), k)
#                 new_binary_message = list(binary_message)
#                 for bit_to_flip in bits_to_flip:
#                     new_binary_message[bit_to_flip] = '1' if binary_message[bit_to_flip] == '0' else '0'
#                     new_message = ''.join(chr(int(''.join(new_binary_message)[i:i+8], 2)) for i in range(0, len(new_binary_message), 8))
#                     new_packet[key] = new_message
#             elif isinstance(value, dict):
#                 new_packet[key] = alter_packet(value)
#             else:
#                 new_packet[key] = value
#             return new_packet
#     else:
#         return packet



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
    
        self.sc = security.certificate()
        
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
                replica = packet
                replica2 = packet
                print(f"Received Packet: {packet}")
                # print(replica)

                lock.acquire()

                replica = json.loads(replica)

                # print(replica)

                replica2 = json.loads(replica2)



                # Alter the replica packet
                new_replica1 = alter_packet(replica)
                # print(replica)

                new_replica = json.dumps(new_replica1)

                # print(replica)


                # for key, value in replica2.items():
                #     if key == "Message":
                #         # alter the message by flipping one random bit
                #         binary_message_packet = ''.join(format(ord(char), '08b') for char in value)

                # for key, value in new_replica1.items():
                #     if key == "Message":
                #         # alter the message by flipping one random bit
                #         binary_message_replica = ''.join(format(ord(char), '08b') for char in value)



                # k = hammingDist(binary_message_packet, binary_message_replica)

                # print(k)

                print(f"Altered Replica Packet: {new_replica}")

                # prompt the user to select which packet to send
                while True:
                    choice = input("Enter 'o' to send the original packet, 'r' to send the replica: ")
                    if choice.lower() == 'o':
                        packet_to_send = packet
                        break
                    elif choice.lower() == 'r':
                        packet_to_send = new_replica
                        # k = hammingDist(binary_message_packet,binary_message_replica)
                        k = hammingDist(packet,new_replica)

                        print("Minimum Hamming distance",k)

                        break
                    else:
                        print('Invalid choice, please try again.')

                packet = packet_to_send 

                lock.release()

                if not packet:
                    print(f"{client_add[0]} just disconnected!")
                    break

                client_socket.send(str.encode(f"Packet Received: {(len(packets))}" ))
                # temp = json.loads(packet)
                if packet:
                    temp = json.loads(packet)
                    # Rest of the code that uses temp
                else:
                    continue

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
                # print("No data in buffer")
                j=0
                

server = Server()
server.start()