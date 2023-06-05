from scapy.all import rdpcap
from scapy.packet import Raw
from scapy.layers.inet import IP
import pandas as pd
import socket

# Define a dictionary to map protocol integer values to string names
protocol_map = {
    1: 'ICMP',
    6: 'TCP',
    17: 'UDP'
}

def process_pcap(file_name):
    # Read the pcap file
    packets = rdpcap(file_name)

    # Create a list to store the packets
    packet_list = []

    # Loop through the packets and add them to the list
    # Loop through the packets and add them to the list
    for packet in packets:
        packet_dict = {}
        for field in packet.fields:
            if field == "proto":
                try:
                    protocol_name = protocol_map.get(packet.fields[field], str(packet.fields[field]))
                    packet_dict['protocol'] = protocol_name
                    continue
                except OSError:
                    # If the protocol is not found, use the integer value
                    packet_dict['protocol'] = packet.fields[field]

            packet_dict[field] = packet.fields[field]
        
        # Extract the payload
        if packet.haslayer(Raw):
            payload = packet[Raw].load
            packet_dict['payload'] = payload
        
        packet_list.append(packet_dict)
        
        packet_list.append(packet_dict)

        # Extract the timestamp
        timestamp = packet.time
        packet_dict['timestamp'] = timestamp
        
        packet_list.append(packet_dict)

    return packet_list


# Example usage
packet_list = process_pcap('messages_http.pcap')

# Assuming packet_list is the list of packet dictionaries
df = pd.DataFrame(packet_list)

# Write the DataFrame to an Excel file
df.to_excel('excel\packets.xlsx', index=False)