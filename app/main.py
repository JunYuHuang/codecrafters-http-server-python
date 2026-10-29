import socket

HOST = "localhost"
PORT = 4221
REQUEST_BUFFER = 1024

def parse_http_request(request: bytes) -> dict:
    res = { "request_line": {} }
    crlf = b'\r\n'

    # Parse request line or start-line
    request_line_end_pos = request.find(crlf)
    request_line_parts = request[:request_line_end_pos].split(b' ')
    res["request_line"]["method"] = request_line_parts[0].decode()
    res["request_line"]["request_target"] = request_line_parts[1].decode()
    res["request_line"]["protocol"] = request_line_parts[2].decode()

    # TODO: Parse headers
    # TODO: Parse body

    return res

def main():
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    server_socket.listen()
    print(f"==> HTTP Server running at {(HOST, PORT)}")

    while True:
        # `client_address` = (host: string, port: integer)
        client_socket, client_address = server_socket.accept()
        print(f"==> HTTP Client at {client_address} connected")

        request_bytes = client_socket.recv(REQUEST_BUFFER)
        request_dict = parse_http_request(request_bytes)
        print(f"==> HTTP Client sent request:\n{request_bytes}")

        request_path = "/"
        if request_dict:
            request_path = request_dict["request_line"]["request_target"]

        response = b'HTTP/1.1 404 Not Found\r\n\r\n'
        if request_path == "/":
            response = b'HTTP/1.1 200 OK\r\n\r\n'

        client_socket.sendall(response)
        print(f"==> Sent response to HTTP Client at {client_address}:\n{response}")

        client_socket.close()

if __name__ == "__main__":
    main()
