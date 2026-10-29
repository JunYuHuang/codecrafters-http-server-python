# Your Task

In this stage, you'll implement the `/echo/{str}` endpoint, which accepts a string and returns it in the response body.

## Response body

A response body is used to return content to the client. This content may be an entire web page, a file, a string, or anything else that can be represented with bytes.

Your `/echo/{str}` endpoint must return a `200` response, with the response body set to given string, and with a `Content-Type` and `Content-Length` header.

Here's an example of an `/echo/{str}` request:
```
GET /echo/abc HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n
```

And here's the expected response:
```
HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\nabc
```

Here's a breakdown of the response:
```
// Status line
HTTP/1.1 200 OK
\r\n                          // CRLF that marks the end of the status line

// Headers
Content-Type: text/plain\r\n  // Header that specifies the format of the response body
Content-Length: 3\r\n         // Header that specifies the size of the response body, in bytes
\r\n                          // CRLF that marks the end of the headers

// Response body
abc                           // The string from the request
```

The two headers are required for the client to be able to parse the response body. Note that each header ends in a CRLF, and the entire header section also ends in a CRLF.

## Tests

The tester will execute your program like this:
```
$ ./your_program.sh
```

The tester will then send a `GET` request to the `/echo/{str}` endpoint on your server, with some random string.
```
$ curl -v http://localhost:4221/echo/abc
```

Your server must respond with a `200` response that contains the following parts:

- `Content-Type` header set to `text/plain`.
- `Content-Length` header set to the length of the given string.
- Response body set to the given string.

```
HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\nabc
```

## Notes

- For more information about HTTP responses, see the [MDN Web Docs on HTTP requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages#http_responses) or the [HTTP/1.1 specification](https://datatracker.ietf.org/doc/html/rfc9112#name-message).

## How to pass this stage

### 1. Write code to pass this stage

Head over to your editor / IDE and implement your solution.

If you want a quick look at what functions to use or how to structure your code, we recommend looking at [Code Examples](https://app.codecrafters.io/courses/http-server/stages/cn2/code-examples).

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
        - else if `request_path` is `/`,
            - send HTTP `200 OK` response
        - else,
            - send HTTP `404 Not Found` response
        - close `client_socket`