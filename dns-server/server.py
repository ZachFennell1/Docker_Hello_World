import socket

# Helper function to find service's address if on the DNS server's namefile
def find_name(file, service_name):
    response = "Service Not Registered"
    try:
        for line in file:
            if service_name in line:
                response = line.split()[2] + " " + line.split()[3]
    except:
        response = "Server Error"        
    return response

# Helper Fucntion to store addresses in the namefile, first checks if the service address is already
# stored to avoid reproducing the address in case the service restarts
def storage_helper(file, data):
    response = "Stored"
    check = False
    for line in file:
        if data.split()[1] in line:
            check = True
    if check is False:
        try:
            file.write(data + "\n")
        except:
            response = "Fail to Store"
    return response

# Processes recieved messages to the DNS Service
def unpack_message(data):
    command = data.split()[0]
    if "Store" in command:
        with open("namefile", "r+") as file:
            payload = storage_helper(file, data)
            file.close()
        return payload
    if "Get" in command:
        with open("namefile", "r+") as file:
            payload = find_name(file, data.split()[1])
            file.close()
        return payload
    else:
        return "ERROR_BIG_TIME"

# handles processing recieved messages to DNS server and responding to the connection
def server(ipaddr, port):
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

# Driver of the DNS server sets it's port and launches the service
if __name__ == '__main__':
    print("GOING")
    port = 53
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
    try:
        server(ipaddr, port)
    except KeyboardInterrupt:
        pass