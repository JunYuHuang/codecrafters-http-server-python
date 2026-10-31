import os
import os.path
import socket
import sys
import threading

HOST = "localhost"
PORT = 4221
REQUEST_BUFFER = 1024

def parse_http_request(request: bytes) -> dict:
    res = { "request_line": {}, "headers": {}, "body": {} }
    crlf = b'\r\n'
    REQUEST_LEN = len(request)

    # Parse request line or start-line
    request_line_end_pos = request.find(crlf)
    request_line_parts = request[:request_line_end_pos].split(b' ')
    res["request_line"]["method"] = request_line_parts[0].decode()
    res["request_line"]["request_target"] = request_line_parts[1].decode()
    res["request_line"]["protocol"] = request_line_parts[2].decode()

    # Parse headers
    headers_start_pos = request_line_end_pos + 2
    headers_end_pos = request.find(crlf + crlf) - 1

    # Return early if no headers
    if headers_end_pos == -2 or request.find(b': ') == -1:
        return res

    headers = request[headers_start_pos:headers_end_pos + 1].split(crlf)
    for header in headers:
        field, value = header.split(b': ')
        field_str = field.decode().lower()
        res["headers"][field_str] = value.decode()

    # Parse body
    body_start_pos = headers_end_pos + 5

    # Return early if no body
    if res["headers"].get("content-length", 0) == "0" or body_start_pos >= REQUEST_LEN:
        return res

    body_end_pos = body_start_pos + int(res["headers"]["content-length"]) - 1
    res["body"] = request[body_start_pos:body_end_pos + 1]

    return res

def handle_http_client(
    client_socket: socket.socket, client_address: tuple, files_root_dir: str
) -> None:
    request_bytes = client_socket.recv(REQUEST_BUFFER)
    request_dict = parse_http_request(request_bytes)
    print(f"==> HTTP Client sent request:")
    print(request_bytes)
    print(request_dict)

    request_path = "/"
    if request_dict:
        request_path = request_dict["request_line"]["request_target"]

    response = b''
    if len(request_path) >= 6 and request_path[:6] == "/echo/":
        echo_str = request_path[6:]
        echo_str_len = len(echo_str.encode())
        has_accept_encoding_gzip = (
            "accept-encoding" in request_dict["headers"] and
            request_dict["headers"]["accept-encoding"].find("gzip") != -1
        )
        response = b'HTTP/1.1 200 OK\r\n'
        response += b'Content-Type: text/plain\r\n'
        response += b'Content-Length: ' + f"{echo_str_len}".encode() + b'\r\n'
        if has_accept_encoding_gzip:
            response += b'Content-Encoding: gzip\r\n'
        response += b'\r\n'
        response += echo_str.encode()
    elif request_path == "/user-agent":
        user_agent = request_dict["headers"]["user-agent"]
        user_agent_len = len(user_agent.encode())
        response = b'HTTP/1.1 200 OK\r\n'
        response += b'Content-Type: text/plain\r\n'
        response += b'Content-Length: ' + f"{user_agent_len}".encode()
        response += b'\r\n\r\n'
        response += user_agent.encode()
    elif len(request_path) > 6 and request_path[:7] == "/files/":
        method = request_dict["request_line"]["method"]
        filename = request_path[7:]
        file_path = files_root_dir + filename
        response = b''
    
        if method == "POST" and os.path.exists(files_root_dir):
            filename_file = open(file_path, "wb")
            filename_file.write(request_dict["body"])
            filename_file.close()
            response += b'HTTP/1.1 201 Created\r\n'
            response += b'Content-Length: 0\r\n\r\n'
        elif method == "GET" and os.path.exists(file_path):
            response += b'HTTP/1.1 200 OK\r\n'
            response += b'Content-Type: application/octet-stream\r\n'
            file_size = os.stat(file_path).st_size
            response += b'Content-Length: ' + f"{file_size}".encode()
            response += b'\r\n\r\n'
            filename_file = open(file_path, "rb")
            response += filename_file.read()
            filename_file.close()
        else:
            response += b'HTTP/1.1 404 Not Found\r\n'
            response += b'Content-Length: 0\r\n\r\n'
    elif request_path == "/":
        response = b'HTTP/1.1 200 OK\r\n'
        response += b'Content-Length: 0\r\n\r\n'
    else:
        response = b'HTTP/1.1 404 Not Found\r\n'
        response += b'Content-Length: 0\r\n\r\n'

    client_socket.sendall(response)
    print(f"==> Sent response to HTTP Client at {client_address}:\n{response}")

    client_socket.close()

def main():
    files_root_dir = "/"
    if len(sys.argv) == 3 and sys.argv[1] == "--directory":
        files_root_dir = sys.argv[2]
        
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    server_socket.listen()
    print(f"==> HTTP Server running at {(HOST, PORT)}")

    while True:
        # `client_address` = (host: string, port: integer)
        client_socket, client_address = server_socket.accept()
        print(f"==> HTTP Client at {client_address} connected")

        handle_client_thread = threading.Thread(
            target=handle_http_client,
            args=(client_socket, client_address, files_root_dir)
        )
        handle_client_thread.start()

if __name__ == "__main__":
    main()
