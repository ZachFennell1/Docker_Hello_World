import socket

# Handles providing the DNS server with the address of this service
def dns_broadcast(ipaddr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    while True:
        try:
            sock.connect(("10.5.0.2", 53))
        except:
            continue
        break
    sock.sendall(b"Store Broker " + ipaddr.encode() + b" " + str(port).encode())
    response = sock.recv(1024).decode()
    sock.close()
    print(response)


# Packs the payload to send to the frontend Server
def payload_packing(command):
    payload = None
    if "World" in command:
        payload = 'HTTP/1.0 200 OK\nAccess-Control-Allow-Origin: *\n\nWorld'
    elif "Hello" in command:
        payload = 'HTTP/1.0 200 OK\nAccess-Control-Allow-Origin: *\n\nHello'
    else:
        payload = "ERROR_BIG_TIME"
    return payload

# Helper Function for requesting the address of a service from the DNS server
def get_address(service):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    while True:
        try:
            sock.connect(("10.5.0.2", 53))
        except:
            continue
        break
    sock.sendall(b"Get " + service.encode())
    response = str(sock.recv(1024).decode())
    print (response, type(response))
    address = (response.split()[0], int(response.split()[1]))
    sock.close()
    return address

# processes recieved messages 
def unpack_message(data):
    command = data.split()[1]

    # handles broker recieving a World request, first it queries the DNS 
    # server for the World service's address, then acts as it's client to get
    # the payload to send to the frontend server
    if "World" in command:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        service = get_address("World")
        sock.connect(service)
        sock.sendall(b"HTTP/1.0 200 OK\nAccess-Control-Allow-Origin: *\n\nWorld")
        response = sock.recv(1024).decode()
        payload = payload_packing(response)
        sock.close()
        return payload

    # handles broker recieving a Hello request, first it queries the DNS 
    # server for the World service's address, then acts as it's client to get
    # the payload to send to the frontend server
    elif "Hello" in command:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        service = get_address("Hello")
        sock.connect(service)
        sock.sendall(b"HTTP/1.0 200 OK\nAccess-Control-Allow-Origin: *\n\nHello")
        response = sock.recv(1024).decode()
        payload = payload_packing(response)
        sock.close()
        return payload
    else:
        return "ERROR_BIG_TIME"

# handles processing recieved messages to broker and responding to the connection
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

# Driver of the broker sets it's port, calls the broadcast to the DNS server, and launches the service
if __name__ == '__main__':
    print("GOING")
    port = 9000
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
    dns_broadcast(ipaddr, port)
    try:
        server(ipaddr, port)
    except KeyboardInterrupt:
        pass