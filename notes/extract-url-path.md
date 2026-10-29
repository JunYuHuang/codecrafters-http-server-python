# Your Task

In this stage, your server will extract the URL path from an HTTP request, and respond with either a `200` or `404`, depending on the path.

## HTTP request

An HTTP request is made up of three parts, each separated by a [CRLF](https://developer.mozilla.org/en-US/docs/Glossary/CRLF) (`\r\n`):

1. Request line.
2. Zero or more headers, each ending with a CRLF.
3. Optional request body.

Here's an example of an HTTP request:
```
GET /index.html HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n
```

Here's a breakdown of the request:
```
// Request line
GET                          // HTTP method
/index.html                  // Request target
HTTP/1.1                     // HTTP version
\r\n                         // CRLF that marks the end of the request line

// Headers
Host: localhost:4221\r\n     // Header that specifies the server's host and port
User-Agent: curl/7.64.1\r\n  // Header that describes the client's user agent
Accept: */*\r\n              // Header that specifies which media types the client can accept
\r\n                         // CRLF that marks the end of the headers

// Request body (empty)
```

The "request target" specifies the URL path for this request. In this example, the URL path is `/index.html`.

Note that each header ends in a CRLF, and the entire header section also ends in a CRLF.

## Tests

The tester will execute your program like this:
```
$ ./your_program.sh
```

The tester will then send two HTTP requests to your server.

First, the tester will send a `GET` request, with a random string as the path:
```
$ curl -v http://localhost:4221/abcdefg
```

Your server must respond to this request with a `404` response:
```
HTTP/1.1 404 Not Found\r\n\r\n
```

Then, the tester will send a `GET` request, with the path `/`:
```
$ curl -v http://localhost:4221
```

Your server must respond to this request with a `200` response:
```
HTTP/1.1 200 OK\r\n\r\n
```

## Notes

- You can ignore the headers for now. You'll learn about parsing headers in a later stage.
- In this stage, the request target is written as a URL path. But the request target actually has [four possible formats](https://datatracker.ietf.org/doc/html/rfc9112#section-3.2). The URL path format is called the "origin form," and it's the most commonly used format. The other formats are used for more niche scenarios, like sending a request through a proxy.
- For more information about HTTP requests, see the [MDN Web Docs on HTTP requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages#http_requests) or the [HTTP/1.1 specification](https://datatracker.ietf.org/doc/html/rfc9112#name-message).

## How to pass this stage

### 1. Write code to pass this stage

Head over to your editor / IDE and implement your solution.

If you want a quick look at what functions to use or how to structure your code, we recommend looking at [Code Examples](https://app.codecrafters.io/courses/http-server/stages/ih0/code-examples).

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
        - set string `request_path` to `request_dict["header"]["request_target"]`
        - if `request_path` is `/`,
            - send HTTP `200 OK` response
        - else,
            - send HTTP `404 Not Found` response
        - close `client_socket`