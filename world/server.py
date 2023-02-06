import socket
import struct
from http.server import HTTPServer, SimpleHTTPRequestHandler, test

# Handles providing the DNS server with the address of this service
def dns_broadcast(ipaddr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    while True:
        try:
            sock.connect(("10.5.0.2", 53))
        except:
            continue
        break
    sock.sendall(b"Store World " + ipaddr.encode() + b" " + str(port).encode())
    response = sock.recv(1024).decode()
    sock.close()
    print(response)

# packs responses to clients that connected to the hello service
def payload_packing(command):
    payload = None
    if "World" in command:
        payload = 'HTTP/1.0 200 OK\nAccess-Control-Allow-Origin: *\n\nWorld'
    else:
        payload = "ERROR_BIG_TIME"
    return payload

# Processes recieved messages to the hello service
def unpack_message(data):
    command = data.split()[-1]
    if "World" in command:
        payload = payload_packing(command)
        return payload
    else:
        return "ERROR_BIG_TIME"

# handles processing recieved messages to hello service and responding to the connection
def server(ipaddr, port):
    sessionid = None
    try:
        print("Open")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((ipaddr, port))
        sock.listen()
        print("Listen")
        while 1:
            conn, addr = sock.accept()
            print("accepted")
            recieved_data = conn.recv(1024).decode()
            payload = unpack_message(recieved_data)
            print(payload)
            conn.sendall(payload.encode())
            conn.close()
        sock.close()
    except socket.error as e:
        print("Socket Error {}".format(e))

# Driver of the World service sets it's port, calls the broadcast to the DNS server, and launches the service
if __name__ == '__main__':
    print("GOING")
    port = 9200
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
    dns_broadcast(ipaddr, port)
    try:
        server(ipaddr, port)
    except KeyboardInterrupt:
        pass