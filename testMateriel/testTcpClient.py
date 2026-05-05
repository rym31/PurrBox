import socket

PORT = 8888
DEST_IP = "192.168.13.1"
MESSAGE = "abcdefg!\n"

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initialize the destination address
dest_addr = (DEST_IP, PORT)

# Create the connection
sock.connect(dest_addr)

# Send the message and close the connection
sock.send(MESSAGE.encode())
sock.close()