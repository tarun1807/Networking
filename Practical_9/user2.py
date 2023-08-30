import random 
import pickle 
import os 

effected_packets = 0

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
    
    new_message = temp+'0' * (len(string2) - len(crc)-1)+crc

    if crc == "0":
   
        return "Passed"

    else :
        
        global effected_packets
        effected_packets += 1
        return "Failed"

    
if __name__ == '__main__': 
    main_data_file = open("my_message.txt", 'r') 
    main_data_file_data = main_data_file.readline() # reading Line 
    main_data_file.close()
    main_data_list = main_data_file_data.split(" ")
        
    message_name = main_data_list[0]
    number_of_framents = int(main_data_list[1])
    recover_file = open(message_name[:message_name.find(".")] + "_recovered_" + message_name[message_name.find(".") : ], 'wb')
    random_set={}
    j=int(input("Want to introduce intentional error in random no. of packets \n1. Yes\n2. No\n"))
    if j==1:
        k = number_of_framents-1   # range of values to choose from
        n = random.randint(1,k)
        random_set = set(random.sample(range(k), n))

        print(f'Random set: {random_set}')

    for i in range(0, number_of_framents): 
        file_name = 'buffer/' + message_name + "_num_enc" + str(i) + ".dat"
        
        with open(file_name, 'rb') as f:
            binary_data = f.read()

        original_string = pickle.loads(binary_data)
        print("___________________________________________________________________")
        
        if i not in random_set:
            print(f'CRC Check {crc(original_string,"1001")} for packet {i} ')

        else:
            print(f'CRC Check {crc(original_string,"11111")} for packet {i} ')

        print("___________________________________________________________________")

    # Do something with the binary data here
    print("\n\n\n")
    print(f'Total no. of packets: {number_of_framents}')
    print(f'Effected packets    : {effected_packets}')
    print(f'Uneffected packets  : {number_of_framents - effected_packets}')

    print("\n\n\n")
    if effected_packets==0:
        j=int(input("No effected packet do you want to receive the message \n1. Yes\n2. No\n"))
        if j==1:
            for i in range(0, number_of_framents): 
                file_name = 'buffer/' + message_name + "_num_" + str(i) + ".dat"
                file = open(file_name, 'rb')
                custPacket = pickle.load(file)
                file.close()
                recover_file.write(custPacket.payload)
            recover_file.close()   

            print("The original message is recovered !\n")

        else:
            print("Have a Good Day\n")


    else:
        print(f'As there are {effected_packets} effected packets original message can not be retrieved')

 

