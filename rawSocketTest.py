import socket
import struct


def connect_to_opc_ua_server(server_ip, server_port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = (server_ip, server_port)
    print(f"Connecting to {server_ip}:{server_port}")
    sock.connect(server_address)

    try:
        # Send a simple Hello message (this is NOT OPC UA compliant, just for illustration)
        hello_message = struct.pack("!I", 0)  # Placeholder for an actual OPC UA message
        sock.sendall(hello_message)

        # Receive a response (again, just for illustration)
        response = sock.recv(1024)
        print(f"Received: {response}")

    finally:
        # Close the connection
        print("Closing connection")
        sock.close()


# Example usage
connect_to_opc_ua_server("milo.digitalpetri.com", 62541)
