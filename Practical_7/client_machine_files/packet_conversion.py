import packet
import math

class packet_convert:
    def __init__(self, message, payload, server_name, server_add, client_name, client_add, username, passwd, msg):
        self.message = message
        self.payload = payload
        
        self.server_name = server_name
        self.server_add = server_add
        self.client_name = client_name
        self.client_add = client_add
        self.msg = msg
        self.username = username
        self.passwd = passwd

        self.packet_store = []
        
    def convert_to_packet(self):
        self.packet_num = len(self.message)//self.payload + math.ceil(len(self.message)%self.payload/self.payload)
        self.ind = 0

        for i in range(self.packet_num):
            self.packet = packet.pack(self.server_name, self.server_add, self.client_name, self.client_add)
            self.packet = packet.pack.gen_packet(self.packet)
            self.packet_message = ""
            
            for j in range(self.payload):
                if self.ind>=len(self.message):
                    break
                self.packet_message += self.message[self.ind]
                self.ind += 1
                
            self.packet["Message"] = self.packet_message
            
            self.packet["Certificate"] = {"Username" : self.username, "Password" : self.passwd}
            self.packet["Type"] = self.msg
            
            self.packet["Number of Packets"] = self.packet_num
            
            self.packet_store.append(self.packet)
        packet.packet_id = -1
        return self.packet_store

