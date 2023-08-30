import random 
import pickle 
import os

class Connection: 

    def __init__(self): 
        self.source_ip_address = None
        self.client_id = None 
        self.destination_ip_address = None 

    def __str__(self): 
        print(f"TESTING..")

class Packet: 

    def __init__(self): 
        self.client_id = None 
        self.client_ip_address = None 
        self.source_ip_address = None 
        self.size_of_payload = None 
        self.number_of_packet = None 
        self.message_name = None 
        self.payload = None 
        self.packet_id = None 
        self.security_certificate = None 

    def __str__(self): 
        return f"{self.payload}"

def makeFragment(string_data, number_of_fragments, connection, file_name): 
    file = open(file_name, 'rb') 
    file_size = os.stat(file_name).st_size 

    number_of_char_in_each_fragments = file_size // number_of_fragments
    last_frament_size = file_size - (number_of_char_in_each_fragments*(number_of_fragments - 1))
    
    list_of_fragments = []
    
    file.seek(0)
    for i in range(0, number_of_fragments): 
        packet = Packet()
        packet.client_id = connection.client_id 
        packet.client_ip_address = connection.destination_ip_address 
        packet.source_ip_address = connection.source_ip_address 
        packet.number_of_packet = number_of_fragments
        packet.message_name = file_name 
        packet.packet_id = i 
        if i == (number_of_fragments - 1):
            data = file.read(number_of_char_in_each_fragments)
            packet.payload = data 
            file.seek(number_of_char_in_each_fragments, 1)
        else:
            data = file.read(last_frament_size)
            packet.payload = data 
        list_of_fragments.append(packet)

    file.close()  

    return list_of_fragments 

def dataFromFragments(list_of_fragments): 
    string_data = ""
    for frg in list_of_fragments: 
        string_data += frg.payload 
    return string_data

if __name__ == '__main__': 
    file_name_frag = input("Enter the file name to be divided into packets : ")
    number_of_packet = int(input("Enter the no. of Packets : "))
    connection = Connection()
    connection.client_id = random.randint(1, 100)
    connection.source_ip_address = "127.0.0.1"
    connection.destination_ip_address = "127.0.01"
    list_of_packet_to_send = makeFragment(None, number_of_packet, connection, file_name_frag)

    main_data_file = open("my_message.txt", 'w') 
    main_data_file.write(f"{file_name_frag} {number_of_packet}")
    main_data_file.close()

    for i in range(0, len(list_of_packet_to_send)): 
        file_name = ""
        file_name = file_name_frag + "_num_" + str(i) + ".dat"
        file = open(file_name, 'wb')
        pickle.dump(list_of_packet_to_send[i], file)
        file.close()
    