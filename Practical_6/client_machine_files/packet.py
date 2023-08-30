packet_id = -1
class pack:
    
    def __init__(self, server_name, server_add, client_name, client_add):
        global packet_id
        self.server_name = server_name
        self.server_add = server_add
        self.client_name = client_name
        self.client_add = client_add
        
        self.message_name = f"{self.server_name} to {self.client_name}"
        packet_id += 1
        
    def gen_packet(self):
        self.packet = {"Client Name" : self.client_name, "Client IP Address" : self.client_add, "Server IP Address" : self.server_add, "Server Name" : self.server_name, "Message Name" : self.message_name, "Packet ID" : packet_id}
        return self.packet
