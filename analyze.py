from scapy.all import rdpcap
from scapy.packet import Raw
from scapy.layers.http import HTTPResponse
import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse

# Define a dictionary to map protocol integer values to string names
protocol_map = {
    1: 'ICMP',
    6: 'TCP',
    17: 'UDP'
}

parser = argparse.ArgumentParser()
parser.add_argument('--mode', type=str, required=True)
parser.add_argument('--criteria', type=str, required=False)
args = parser.parse_args()
print('mode:', args.mode)

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

        # Extract the Content-Type header from response packets
        if packet.haslayer(HTTPResponse):
            http_layer = packet[HTTPResponse]
            content_type = http_layer.fields.get('Content-Type')
            if content_type:
                packet_dict['Content-Type'] = content_type


        packet_list.append(packet_dict)

    return packet_list


# This pcap is UNencrypted stego objects with embed messages
packet_list_http = process_pcap('pcaps/http/stego_http.pcap')
# This pcap is the encrypted non-stego message objects 
packet_list_tls = process_pcap('pcaps/https/messages_https.pcap')
# This pcap is encrypted stego objects
packet_list_tls = process_pcap('pcaps/https/stego_https.pcap')

# Store in pandas DF
df_http = pd.DataFrame(packet_list_http)
df_tls = pd.DataFrame(packet_list_tls) 
df_stego_tls = pd.DataFrame(packet_list_tls)

# Write the DataFrames to an Excel file
df_http.to_excel('excel\http_packets.xlsx', index=False)
df_tls.to_excel('excel\https_packets.xlsx', index=False)
df_stego_tls.to_excel('excel\https_stego_packets.xlsx', index=False)

if (args.mode == 'http'):
    if(args.criteria == 'protocol'):
        # chart protocol occurences
        protocol_counts = df_http['protocol'].value_counts()
        # Plot the data as a bar chart
        protocol_counts.plot(kind='bar')
        plt.xlabel('Protocol')
        plt.ylabel('Number of Occurrences')
        plt.show()
    elif(args.criteria == 'count'):
        max_timestamp = df_http['timestamp'].max()
        # Define a function to compute the relative time
        def compute_relative_time(timestamp):
            return max_timestamp - timestamp
        df_http['relative_time'] = df_http['timestamp'].apply(compute_relative_time)
        # Assuming df is the DataFrame containing the data
        fig, ax = plt.subplots()

        # Create a scatter plot of the data
        ax.scatter(df_http['relative_time'], df_http['len'])

        # Set the axis labels
        ax.set_xlabel('Time')
        ax.set_ylabel('Byte Length')

        plt.title("Distribution of packets by byte-length across time elapsed (http-stego)")
        # Show the plot
        plt.show()

elif(args.mode == 'tls'):
    if(args.criteria == 'protocol'):
        # chart protocol occurences
        protocol_counts = df_tls['protocol'].value_counts()
        # Plot the data as a bar chart
        protocol_counts.plot(kind='bar')
        plt.xlabel('Protocol')
        plt.ylabel('Number of Occurrences')
        plt.show()
    
    elif(args.criteria == 'count'):
        max_timestamp = df_tls['timestamp'].max()
        # Define a function to compute the relative time
        def compute_relative_time(timestamp):
            return max_timestamp - timestamp
        df_tls['relative_time'] = df_tls['timestamp'].apply(compute_relative_time)
        # Assuming df is the DataFrame containing the data
        fig, ax = plt.subplots()

        # Create a scatter plot of the data
        ax.scatter(df_tls['relative_time'], df_tls['len'])

        # Set the axis labels
        ax.set_xlabel('Time')
        ax.set_ylabel('Byte Length')

        plt.title("Distribution of packets by byte-length across time elapsed (tls non-stego)")
        # Show the plot
        plt.show()

elif(args.mode == 'stegoTLS'):
    if(args.criteria == 'protocol'):
        # chart protocol occurences
        protocol_counts = df_stego_tls['protocol'].value_counts()
        # Plot the data as a bar chart
        protocol_counts.plot(kind='bar')
        plt.xlabel('Protocol')
        plt.ylabel('Number of Occurrences')
        plt.show()
    elif(args.criteria == 'count'):
        max_timestamp = df_stego_tls['timestamp'].max()
        # Define a function to compute the relative time
        def compute_relative_time(timestamp):
            return max_timestamp - timestamp
        df_stego_tls['relative_time'] = df_stego_tls['timestamp'].apply(compute_relative_time)
        # Assuming df is the DataFrame containing the data
        fig, ax = plt.subplots()

        # Create a scatter plot of the data
        ax.scatter(df_stego_tls['relative_time'], df_stego_tls['len'])

        # Set the axis labels
        ax.set_xlabel('Time')
        ax.set_ylabel('Byte Length')

        plt.title("Distribution of packets by byte-length across time elapsed (tls w/stego)")
        # Show the plot
        plt.show()

elif(args.mode == "totalCounts"):
    # Assuming df1, df2, and df3 are the three DataFrames
    num_rows = pd.DataFrame({
        'DataFrame': ['Stego_only', 'TLS_only', 'Stego w/TLS'],
        'Number of Rows': [df_http.shape[0], df_tls.shape[0], df_stego_tls.shape[0]]
    })

    # Plot the data as a bar chart
    num_rows.plot(x='DataFrame', y='Number of Rows', kind='bar')
    plt.xlabel('DataFrame')
    plt.ylabel('Number of Rows')
    plt.title("Packet counts for 300s capture of Pseudo-Random Net Activity")
    plt.show()

elif(args.mode == "totalSizes"):


    file_paths = ['pcaps/http/stego_http.pcap', 'pcaps/https/messages_https.pcap', 'pcaps/https/stego_https.pcap']
    
    # Get the file sizes
    file_sizes = [os.path.getsize(file_path) for file_path in file_paths]

    file_names = ["Stego-only", "TLS-only", "Stego w/TLS"]

    # Create the bar chart
    plt.bar(file_names, file_sizes)
    plt.xlabel('Mode')
    plt.ylabel('File Size (MB)')
    plt.title("Method by file size")
    plt.show()

elif(args.mode == "totalProtocols"):

    # Assuming df1, df2, and df3 are the three DataFrames
    protocol_counts1 = df_http['protocol'].value_counts()
    protocol_counts2 = df_tls['protocol'].value_counts()
    protocol_counts3 = df_stego_tls['protocol'].value_counts()

    # Concatenate the three Series into a single DataFrame
    protocol_counts = pd.concat([protocol_counts1, protocol_counts2, protocol_counts3], axis=1)
    protocol_counts.columns = ['stego', 'tls', 'stego+tls']

    # Plot the data as a bar chart
    protocol_counts.plot(kind='bar')
    plt.xlabel('Protocol')
    plt.ylabel('Number of Occurrences')
    plt.title("Protocol counts by method")
    plt.show()



