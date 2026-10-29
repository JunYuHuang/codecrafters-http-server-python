# Your Task

In this stage, you'll implement the `/user-agent` endpoint, which reads the `User-Agent` request header and returns it in the response body.

## The `User-Agent` header

The [`User-Agent`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent) header describes the client's user agent.

Your `/user-agent` endpoint must read the `User-Agent` header, and return it in your response body. Here's an example of a `/user-agent` request:
```
// Request line
GET
/user-agent
HTTP/1.1
\r\n

// Headers
Host: localhost:4221\r\n
User-Agent: foobar/1.2.3\r\n  // Read this value
Accept: */*\r\n
\r\n

// Request body (empty)
```

Here is the expected response:
```
// Status line
HTTP/1.1 200 OK               // Status code must be 200
\r\n

// Headers
Content-Type: text/plain\r\n
Content-Length: 12\r\n
\r\n

// Response body
foobar/1.2.3                  // The value of `User-Agent`
```

## Tests

The tester will execute your program like this:
```
$ ./your_program.sh
```

The tester will then send a `GET` request to the `/user-agent` endpoint on your server. The request will have a `User-Agent` header.
```
$ curl -v --header "User-Agent: foobar/1.2.3" http://localhost:4221/user-agent
```

Your server must respond with a `200` response that contains the following parts:

- `Content-Type` header set to `text/plain`.
- `Content-Length` header set to the length of the `User-Agent` value.
- Message body set to the `User-Agent` value.

```
HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 12\r\n\r\nfoobar/1.2.3
```

## Notes

- Header names are [case-insensitive](https://datatracker.ietf.org/doc/html/rfc9112#name-field-syntax).

## How to pass this stage

### 1. Write code to pass this stage

Head over to your editor / IDE and implement your solution.

If you want a quick look at what functions to use or how to structure your code, we recommend looking at [Code Examples](https://app.codecrafters.io/courses/http-server/stages/fs3/code-examples).

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
        - TODO
    - notes
        - for this stage, can assume request target in HTTP Request header follows the `origin-form` format per [RFC-9112](https://datatracker.ietf.org/doc/html/rfc9112#section-3.2)
        - server program can handle multiple HTTP requests from multiple HTTP clients
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
- PEDAC: Data Structures And Algorithms
    - helper functions:
        - `parse_http_request(request: bytes) -> hashmap`
            - converts `request` to a string from bytes
            - returns a hashmap that maps all the HTTP request components from `request` to their associated string keys and string values
    - server creates a TCP socket that binds to a host and port
    - server listens for TCP clients
    - in an infinite loop,
        - set `client_socket` object that represents HTTP client's TCP socket connection
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
        - else if `request_path` is `/`,
            - send HTTP `200 OK` response
        - else,
            - send HTTP `404 Not Found` response
        - close `client_socket`