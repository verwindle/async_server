import socket


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 8080))
    server_socket.listen()


    while True:
        client_socket, addr = server_socket.accept()
        print('Connection established from {}'.format(addr))
        greetings = 'server is listening\n'.encode()
        client_socket.send(greetings)
        while True:
            request = client_socket.recv(4096)

            if not request:
                break
            else:
                response = 'knock knock\n'.encode()
                client_socket.send(response)

        client_socket.close()
        print('Connection closed')

server()