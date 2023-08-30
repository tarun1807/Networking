import random 
import pickle 
import os
import math


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

def crc(string1,string2):
    # generator_poly = '1001'
    generator_poly = string2
    # message = '1010000000'
    message = string1
    tm=string1
    temp = message

    message += '0' * (len(generator_poly) - 1)
    tm1=message

    message_dec = int(message, 2)
    generator_poly_dec = int(generator_poly, 2)

    while message_dec >= generator_poly_dec:
        shift = len(bin(message_dec)) - len(bin(generator_poly_dec))
        shifted_poly = generator_poly_dec << shift

        message_dec = message_dec ^ shifted_poly

    crc = bin(message_dec)[2:]
    # print(message)
    print(crc)
    new_message = temp+'0' * (len(string2) - len(crc)-1)+crc

    # new_message = bin(int(crc, 2) + int(temp, 2))[2:]
    # new_message=tm[:len(tm)-len(str(crc))]+str(crc)

    # print(new_message)

    return new_message,tm1


if __name__ == '__main__': 

    connection = Connection()
    connection.client_id = random.randint(1, 100)
    print("Client ID: ",connection.client_id)
    # connection.source_ip_address = "127.0.0.1"
    # connection.destination_ip_address = "127.0.01"
    connection.source_ip_address = input("Enter Source IP address : ")
    connection.destination_ip_address = input("Enter Destination IP address : ")



    file_name_frag = input("Enter the file name to be divided into packets : ")
    file_size = os.path.getsize(file_name_frag)
    number_of_payload = int(input("Enter the Payload : "))
    number_of_packet =  math.ceil(file_size / number_of_payload)
    print("No. of Packets calculated =")
    print(number_of_packet)

    
    list_of_packet_to_send = makeFragment(None, number_of_packet, connection, file_name_frag)

    main_data_file = open("my_message.txt", 'w') 
    main_data_file.write(f"{file_name_frag} {number_of_packet}")
    main_data_file.close()


    # Create the buffer folder if it does not exist
    if not os.path.exists("buffer"):
        os.makedirs("buffer")


    for i in range(0, len(list_of_packet_to_send)): 

        print(f"\nOriginal payload data of packet {i}: {list_of_packet_to_send[i].payload}")
        # print(type(list_of_packet_to_send[i].payload))
        binary_string = bin(int.from_bytes(list_of_packet_to_send[i].payload, byteorder='big'))[2:]
        # print(binary_string)
        print(f"Original    dataframe{i}: {binary_string}")
        # print("here")
        # print(type(binary_string))
        # print("there")
        # j=crc("1010000000","1001")

        j,p=crc(binary_string,"1001")


        file_name = ""
        file_name = "buffer\\" + file_name_frag + "_num_enc" + str(i) + ".dat"
        file = open(file_name, 'wb')
        pickle.dump(j, file)
        file.close()

        file_name = ""
        file_name = "buffer\\" + file_name_frag + "_num_" + str(i) + ".dat"
        file = open(file_name, 'wb')
        pickle.dump(list_of_packet_to_send[i], file)
        file.close()

        # print("here")
        # print(j)
        print(f"Mssg Original dataframe{i} : {p}")
        print(f"CRC encoded   dataframe{i} : {j}\n")



    