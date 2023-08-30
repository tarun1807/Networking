import shutil
import random
import pickle
import os
import time
import random

from datetime import datetime

folder_path = 'sender'
folder_path2 = 'receiver'


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
    last_frament_size = file_size - \
        (number_of_char_in_each_fragments*(number_of_fragments - 1))

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
    receiver_window_size = int(input("Enter the receiver window size: "))
    main_data_file = open("my_message.txt", 'r')
    main_data_file_data = main_data_file.readline()  # reading Line
    main_data_file.close()

    ssize = open("ssize.txt", 'r')
    ssize_data = int(ssize.readline())  # reading Line
    ssize.close()

    psize = open("pack.txt", 'r')
    psize_data = int(psize.readline())  # reading Line
    psize.close()

    # print(ssize_data)

    main_data_list = main_data_file_data.split(" ")
    message_name = main_data_list[0]
    number_of_fragments = int(main_data_list[1])

    # Get the smaller size between ssize_data and receiver_window_size
    smaller_size = min(ssize_data, receiver_window_size)

    # Create the receive folder if it does not exist
    if not os.path.exists("receiver"):
        os.makedirs("receiver")

    # Add packets to receive folder
    packets_added = 0

    # print(number_of_fragments)
    j =  0
    error_packet = int(input("Enter the packet number where you want to introduce an error (Enter -1 to not introduce any error): "))
    

    while packets_added < number_of_fragments:
        # Get the number of packets to add in this iteration
        packets_to_add = min(number_of_fragments - packets_added, smaller_size)
        k=packets_to_add
        for i in range(packets_to_add):
            start_time = time.time()

            

            j+=1

            if (j!=error_packet):
                k-=1

                src_file = 'sender/' + message_name + \
                    "_num_" + str(packets_added + i) + ".dat"
                dest_file = 'receiver/' + message_name + \
                    "_num_" + str(packets_added + i) + ".dat"
                shutil.copy(src_file, dest_file)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # get the current timestamp
                packett_size = os.path.getsize(dest_file)
                end_time = time.time()  # record the end time
                receive_time = end_time - start_time  # calculate the receive time
                print(f"[{timestamp}] Received {src_file} of size {packett_size} bytes in {receive_time:.2f} seconds")

            else:
                packets_added -=k
                break

        packets_added += packets_to_add

        

        packets_received = os.listdir('receiver')
        packets_received.sort(key=lambda x: int(
            x.split("_")[-1].split(".")[0]))
        for i in range(number_of_fragments):
            if f"{message_name}_num_{i}.dat" in packets_received:
                print("X", end=" ")
            else:
                print("O", end=" ")

        time.sleep(2)

        # Check if all packets have been received
        packets_received = os.listdir('receiver')
        if len(packets_received) == number_of_fragments:
            print("All packets sent successfully.\n")
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

            recover_file = open(message_name[:message_name.find(
                ".")] + "_recovered_" + message_name[message_name.find("."):], 'wb')
            for i in range(0, number_of_fragments):
                file_name = 'receiver/' + message_name + \
                    "_num_" + str(i) + ".dat"
                file = open(file_name, 'rb')
                custPacket = pickle.load(file)
                file.close()
                recover_file.write(custPacket.payload)
            recover_file.close()

            print("The original message has been recovered and saved to file.")
            for filename in os.listdir(folder_path2):
                file_path2 = os.path.join(folder_path2, filename)
                try:
                    if os.path.isfile(file_path2) or os.path.islink(file_path2):
                        os.unlink(file_path2)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        else:
            print(
                f"First {packets_added} packets sent successfully. Waiting for remaining packets.\n")
