import socket  # noqa: F401

HOST = "localhost"
PORT = 4221

def main():
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    server_socket.listen()
    print(f"==> HTTP Server running at {(HOST, PORT)}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"==> HTTP Client at {client_address} connected")

        response = b'HTTP/1.1 200 OK\r\n\r\n'
        client_socket.sendall(response)
        print(f"==> Sent message to client at {client_address}:")
        print(response)

if __name__ == "__main__":
    main()
