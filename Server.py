import socket

def start_stun_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f'STUN server started on {host}:{port}')

    first_addr = None
    second_addr = None
    was_first = False

    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f'Received request from {addr}')
        ip, port = addr
        if (not was_first):
            first_addr = addr
        else:
            second_addr = addr
            f_ip, f_port = first_addr
            s_ip, s_port = second_addr
            server_socket.sendto(f'{f_ip}:{f_port}'.encode(), second_addr)
            server_socket.sendto(f'{s_ip}:{s_port}'.encode(), first_addr)
            break
        was_first = True

start_stun_server('111.111.111.111', 3478)
