def receive_messages(socket):
    while True:
        data, addr = socket.recvfrom(1024)
        print(f'Received message from {addr}: {data.decode()}')

def start_client(stun_server_addr, local_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('0.0.0.0', local_port))

    client_socket.sendto(b'GET_OPPONENT_IP', stun_server_addr)
    print('Receiving...')
    data, addr = client_socket.recvfrom(1024)
    pivot = str(data).find(':') - 2 #b'
    public_ip, public_port = data[0:pivot], int(data[pivot+1:])
    print(f'Public IP: {public_ip}, Public Port: {public_port}')

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    other_client_addr = (public_ip, public_port)
    client_socket.sendto(b'Hello from client!', other_client_addr)

    while True:
        message = input()
        client_socket.sendto(message.encode(), other_client_addr)

stun_server_addr = ('111.111.111.111', 3478)
start_client(stun_server_addr, 5000)
