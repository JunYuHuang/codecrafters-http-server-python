# Your Task

In this stage, you'll add support for the `POST` method of the `/files/{filename}` endpoint, which accepts text from the client and creates a new file with that text.

## Request body

A request body is used to send data from the client to the server.

Here's an example of a `POST /files/{filename}` request:
```
// Request line
POST /files/number HTTP/1.1
\r\n

// Headers
Host: localhost:4221\r\n
User-Agent: curl/7.64.1\r\n
Accept: */*\r\n
Content-Type: application/octet-stream  // Header that specifies the format of the request body
Content-Length: 5\r\n                   // Header that specifies the size of the request body, in bytes
\r\n

// Request Body
12345
```

## Tests

The tester will execute your program with a `--directory` flag. The `--directory` flag specifies the directory to create the file in, as an absolute path.
```
$ ./your_program.sh --directory /tmp/
```

The tester will then send a `POST` request to the `/files/{filename}` endpoint on your server, with the following parts:

- `Content-Type` header set to `application/octet-stream`.
- `Content-Length` header set to the size of the request body, in bytes.
- Request body set to some random text.

```
$ curl -v --data "12345" -H "Content-Type: application/octet-stream" http://localhost:4221/files/file_123
```

Your server must return a `201` response:
```
HTTP/1.1 201 Created\r\n\r\n
```

Your server must also create a new file in the files directory, with the following requirements:

- The filename must equal the `filename` parameter in the endpoint.
- The file must contain the contents of the request body.

## How to pass this stage

### 1. Write code to pass this stage

Head over to your editor / IDE and implement your solution.

If you want a quick look at what functions to use or how to structure your code, we recommend looking at [Code Examples](https://app.codecrafters.io/courses/http-server/stages/qv8/code-examples).

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
- PEDAC: Data Structures And Algorithms
    - helper functions:
        - `parse_http_request(request: bytes) -> hashmap`
            - converts `request` to a string from bytes
            - returns a hashmap that maps all the HTTP request components from `request` to their associated string keys and string values
        - `handle_http_client(client_socket: Socket) -> None`
            - set `request_bytes` to bytes (that represent a HTTP Request) received from `client_socket`
            - set hashmap `request_dict` to `parse_http_request(request_bytes)`
            - set string `request_path` to `request_dict["request_line"]["request_target"]`
            - if `request_path` matches regex expression `/echo/{str}`,
                - send HTTP `200 OK` response with:
                    - headers:
                        - `Content-Type` = `text/plain`
                        - `Content-Length` = length of `{str}` in bytes
                    - body:
                        - set to `{str}`
            - if `request_path` is `/user-agent`,
                - set string `user_agent` to `request["headers"]["user-agent"]`
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
