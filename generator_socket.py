import socket
from select import select


tasks = []
to_read, to_write = {}, {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 8080))
    server_socket.listen()

    while True:
        yield ('read', server_socket)
        client_socket, address = server_socket.accept()
        
        print("Connection established from", address)
        tasks.append(client(client_socket))
    

def client(sock):
    while True:

        yield ('read', sock)
        request = sock.recv(4096)

        if request:
            yield ('write', sock)
            response = 'Hi there\n'.encode()
            sock.send(response)
        
    sock.close()
    raise StopIteration
        

def event_loop():
        while any((tasks, to_read, to_write)):
            while not tasks:
                ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

                for sock in ready_to_read:
                    tasks.append(to_read.pop(sock))
                for sock in ready_to_write:
                    tasks.append(to_write.pop(sock))
                
            try:
                task = tasks.pop(0)
                reason, sock = next(task)
                
                if reason == 'read':
                    to_read[sock] = task
                if reason == 'write':
                    to_write[sock] = task

            except StopIteration as err:
                print('all is out', err)


if __name__ == '__main__':
    tasks.append(server())
    event_loop()

