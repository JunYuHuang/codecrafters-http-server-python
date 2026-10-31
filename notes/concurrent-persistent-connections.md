# Your Task

In this stage, you'll extend your server to handle multiple concurrent persistent connections.

## Tests

The tester will execute your program like this:
```
$ ./your_program.sh
```

The tester will create two persistent connections and send multiple requests on each:
```
$ curl --http1.1 -v http://localhost:4221/echo/banana --next http://localhost:4221/user-agent -H "User-Agent: blueberry/apple-blueberry"
```

Your server must:

1. Handle multiple concurrent TCP connections
2. Keep each connection open for multiple requests
3. Process requests independently on each connection
4. Return appropriate responses for all requests

## Notes

- Each connection should be handled independently
- The server should maintain the state of each connection separately
- Requests on different connections can be processed concurrently

## How to pass this stage

### 1. Write code to pass this stage

Head over to your editor / IDE and implement your solution.

If you want a quick look at what functions to use or how to structure your code, we recommend looking at [Code Examples](https://app.codecrafters.io/courses/http-server/stages/ul1/code-examples).

### 2. Submit code

To run tests, make changes to your code and run the submit command:
```
codecrafters submit # Visit https://codecrafters.io/cli to install
```

To run tests, make changes to your code and run the following commands:
```
git add .
git commit --allow-empty -m "[any message]"
git push origin master
```

# Notes:

- PEDAC: Problem
    - input:
        - `http_request`: HTTP Request message sent to the program from an HTTP client, encoded as bytes
    - output:
        - `http_response`: HTTP Response message sent to the HTTP client from the program, encoded as bytes
    - side effects:
        - optional: prints logs to show history of actions
    - questions
        - how to set up HTTP server to support concurrent (non-blocking?) connections?
            - multi-threading; spawn a new thread per TCP (socket) connection when a HTTP client connects to the HTTP server
            - async, non-blocking thread (like Node.js event loop); make receiving from and sending bytes to HTTP clients async to not block the single thread running the HTTP server 
    - notes
        - for this stage, can assume request target in HTTP Request header follows the `origin-form` format per [RFC-9112](https://datatracker.ietf.org/doc/html/rfc9112#section-3.2)
        - server program can handle multiple HTTP requests from multiple HTTP clients
        - HTTP responses should always include `Content-Length` header
        - make CLI argument flag `--directory` optional for starting the HTTP server program
        - 1 TCP connection between HTTP client and HTTP server can support 1+ requests (and 1+ responses)
            - 1 handler per connection
            - 1+ requests per handler
- PEDAC: Examples
    - ex.1
        - start HTTP server program in 1 terminal:
            ```
            ./your_program.sh
            ```
        - send HTTP GET Request to server in another terminal:
            ```
            curl -v http://localhost:4221/abcdefg
            ```
        - HTTP server program responds to client's HTTP request with response:
            ```
            HTTP/1.1 404 Not Found\r\n\r\n
            ```
    - ex.2
        - start HTTP server program in 1 terminal:
            ```
            ./your_program.sh
            ```
        - send HTTP GET Request to server in another terminal:
            ```
            curl -v http://localhost:4221
            ```
        - HTTP server program responds to client's HTTP request with response:
            ```
            HTTP/1.1 200 OK\r\n\r\n
            ```
    - ex.3
        - start HTTP server program in 1 terminal:
            ```
            ./your_program.sh
            ```
        - send HTTP GET Request to server in another terminal:
            ```
            curl -i http://localhost:4221/echo/abc
            ```
        - HTTP server program responds to client's HTTP request with response:
            ```
            HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\nabc
            ```
    - ex.4
        - start HTTP server program in 1 terminal:
            ```
            ./your_program.sh
            ```
        - send HTTP GET Request to server in another terminal:
            ```
            curl -i http://localhost:4221/user-agent
            ```
        - HTTP server program responds to client's HTTP request with response:
            ```
            HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 10\r\n\r\ncurl/8.5.0
            ```
    - ex.5: file `foo` exists on HTTP server at `/tmp/foo`
        - create the file on the HTTP server program:
            ```
            $ echo -n 'Hello, World!' > /tmp/foo
            $ curl -i http://localhost:4221/files/foo
            ```
        - start HTTP server program in 1 terminal:
            ```
            ./your_program.sh --directory /tmp/
            ```
        - send HTTP GET Request to server in another terminal:
            ```
            curl -i http://localhost:4221/files/foo
            ```
        - HTTP server program responds to client's HTTP request with response:
            ```
            HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: 13\r\n\r\nHello, World!
            ```
    - ex.6: file `non_existant_file` exists on HTTP server at `/tmp/foo`
        - start HTTP server program in 1 terminal:
            ```
            ./your_program.sh --directory /tmp/
            ```
        - send HTTP GET Request to server in another terminal:
            ```
            curl -i http://localhost:4221/files/non_existant_file
            ```
        - HTTP server program responds to client's HTTP request with response:
            ```
            HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n
            ```
    - ex.7: create or overwrite file `file_123` on HTTP server at path `/tmp/file_123`
        - start HTTP server program in 1 terminal:
            ```
            ./your_program.sh --directory /tmp/
            ```
        - send HTTP POST Request to server in another terminal:
            ```
            curl -v --data "12345" -H "Content-Type: application/octet-stream" http://localhost:4221/files/file_123
            ```
        - HTTP server program responds to client's HTTP request with response:
            ```
            HTTP/1.1 201 Created\r\nContent-Length: 0\r\n\r\n
            ```
    - ex.8: send Request with valid header `Accept-Encoding: gzip`
        - start HTTP server program in 1 terminal:
            ```
            ./your_program.sh
            ```
        - send HTTP POST Request to server in another terminal:
            ```
            curl -v -H "Accept-Encoding: gzip" http://localhost:4221/echo/abc
            ```
        - HTTP server program responds to client's HTTP request with response:
            ```
            HTTP/1.1 200 OK \r\nContent-Length: {size_in_bytes}\r\nContent-Type: text/plain\r\nContent-Encoding: gzip\r\n\r\n
            ```
    - ex.9: send Request with invalid header `Accept-Encoding: invalid-encdoing`
        - start HTTP server program in 1 terminal:
            ```
            ./your_program.sh
            ```
        - send HTTP POST Request to server in another terminal:
            ```
            curl -v -H "Accept-Encoding: invalid-encoding" http://localhost:4221/echo/abc
            ```
        - HTTP server program responds to client's HTTP request with response:
            ```
            HTTP/1.1 200 OK \r\nContent-Length: {size_in_bytes}\r\nContent-Type: text/plain\r\n\r\n
            ```
    - ex.10: send Request with valid & invalid headers
        - start HTTP server program in 1 terminal:
            ```
            ./your_program.sh
            ```
        - send HTTP POST Request to server in another terminal:
            ```
            curl -v -H "Accept-Encoding: invalid-encoding-1, gzip, invalid-encoding-2" http://localhost:4221/echo/abc
            ```
        - HTTP server program responds to client's HTTP request with response:
            ```
            HTTP/1.1 200 OK \r\nContent-Length: {size_in_bytes}\r\nContent-Type: text/plain\r\nContent-Encoding: gzip\r\n\r\n
            ```
    - ex.11: send Request with invalid headers
        - start HTTP server program in 1 terminal:
            ```
            ./your_program.sh
            ```
        - send HTTP POST Request to server in another terminal:
            ```
            curl -v -H "Accept-Encoding: invalid-encoding-1, invalid-encoding-2" http://localhost:4221/echo/abc
            ```
        - HTTP server program responds to client's HTTP request with response:
            ```
            HTTP/1.1 200 OK \r\nContent-Length: {size_in_bytes}\r\nContent-Type: text/plain\r\n\r\n
            ```
    - ex.12: send Request with header `Accept-Encoding: gzip` and gzip-compressed bytes of a file as a body
        - start HTTP server program in 1 terminal:
            ```
            ./your_program.sh
            ```
        - send HTTP POST Request to server in another terminal:
            ```
            curl -v -H "Accept-Encoding: gzip" http://localhost:4221/echo/abc | hexdump -C
            ```
        - HTTP server program responds to client's HTTP request with response:
            ```
            HTTP/1.1 200 OK \r\nContent-Length: {size_in_bytes}\r\nContent-Type: text/plain\r\nContent-Type: text/plain\r\n{bytes}
            ```
    - ex.13: ??
        - start HTTP server program in 1 terminal:
            ```
            ./your_program.sh
            ```
        - send HTTP POST Request to server in another terminal:
            ```
            curl --http1.1 -v http://localhost:4221/echo/banana --next http://localhost:4221/user-agent -H "User-Agent: blueberry/apple-blueberry"
            ```
        - HTTP server program responds to client's HTTP request with response:
            - ??
            ```
            HTTP/1.1 200 OK \r\nContent-Length: {size_in_bytes}\r\nContent-Type: text/plain\r\nContent-Type: text/plain\r\n{bytes}
            ```
- PEDAC: Data Structures And Algorithms
    - helper functions:
        - `parse_http_request(request: bytes) -> hashmap`
            - converts `request` to a string from bytes
            - returns a hashmap that maps all the HTTP request components from `request` to their associated string keys and string values
        - `handle_http_client(client_socket: Socket) -> None`
            - set bool `should_close_connection` to false
            - set `request_bytes` to bytes (that represent a HTTP Request) received from `client_socket`
            - set hashmap `request_dict` to `parse_http_request(request_bytes)`
            - set string `request_path` to `request_dict["request_line"]["request_target"]`
            - if key `connection` is in `request_dict["headers"]` and `request_dict["headers"]["connection"]` is `close`,
                - set `should_keep_connection` to false
            - if `request_path` matches regex expression `/echo/{str}`,
                - set bool `has_accept_encoding_gzip` to true if key `Accept-Encoding` in `request_dict` and its string value includes `gzip`, else to false
                - set string `str_compressed` to `{str}`
                - build HTTP `200 OK` response:
                    - headers:
                        - `Content-Type` = `text/plain`
                        - if `has_accept_encoding_gzip`,
                            - add header `Content-Encoding: gzip`
                            - `Content-Length` = length of `str_compressed` in bytes
                        - else,
                            - `Content-Length` = length of `{str}` in bytes
                    - body:
                        - if `has_accept_encoding_gzip`,
                            - set to `str_compressed`
                        - else,
                            - set to `{str}`
                - send HTTP response
            - if `request_path` is `/user-agent`,
                - set string `user_agent` to `request_dict["headers"]["user-agent"]`
                - send HTTP `200 OK` response with:
                    - headers:
                        - `Content-Type` = `text/plain`
                        - `Content-Length` = length of `user_agent` in bytes
                    - body:
                        - set to `user_agent`
            - else if `request_path` matches regex `/files/{filename}`,
                - set string `filename` to `{filename}` extracted from `request_path`
                - set string `file_path` to `{files_root_dir}/{filename}`
                - if method is `POST` and `files_root_dir` is valid path,
                    - create the file `filename` at path `file_path` with the contents of the POST Request body's contents
                    - send HTTP `201 Created` response with:
                        - headers:
                            - `Content-Length` = 0
                        - body:
                            - empty
                - else if method is `GET` and file exists at path `file_path`,
                    - send HTTP `200 OK` response with:
                        - headers:
                            - `Content-Type` = `application/octet-stream`
                            - `Content-Length` = content size of file at path `file_path` in bytes
                        - body:
                            - set to UTF-8 textual content of file at path `file_path` encoded as bytes
                - else,
                    - send HTTP `404 Not Found` response with:
                        - headers:
                            - `Content-Length` = 0
                        - body:
                            - empty
            - else if `request_path` is `/`,
                - send HTTP `200 OK` response
            - else,
                - send HTTP `404 Not Found` response
            - if not `should_close_connection`,
                - go to start of function
            - close `client_socket`
    - set `argv` string array to received CLI arguments
    - set `files_root_dir` string to `/`
    - if `argv` length is 3 and `argv[1]` is  `--directory`,
        - set `files_root_dir` string to `argv[2]`
    - server creates a TCP socket that binds to a host and port
    - server listens for TCP clients
    - in an infinite loop,
        - accept the client TCP connection
        - set `client_socket` object that represents HTTP client's TCP socket connection
        - spawn a new thread that runs `handle_http_client(client_socket)`
