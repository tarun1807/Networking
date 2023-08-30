import json
class packet:
    def __init__(self):
        pass

    def convert(self, packet):
        self.packet = json.loads(packet)
        self.msg = self.packet['Message']
        self.pkt_id = self.packet['Packet ID']
        self.pkt_num = self.packet['Number of Packets']

        return self.msg, self.pkt_id, self.pkt_num
         