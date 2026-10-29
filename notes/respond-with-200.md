# Your Task

In this stage, your server will respond to an HTTP request with a `200` response.

## HTTP response

An HTTP response is made up of three parts, each separated by a [CRLF](https://developer.mozilla.org/en-US/docs/Glossary/CRLF) (`\r\n`):

1. Status line.
2. Zero or more headers, each ending with a CRLF.
3. Optional response body.

In this stage, your server's response will only contain a status line. Here's the response your server must send:
```
HTTP/1.1 200 OK\r\n\r\n
```

Here's a breakdown of the response:
```
// Status line
HTTP/1.1  // HTTP version
200       // Status code
OK        // Optional reason phrase
\r\n      // CRLF that marks the end of the status line

// Headers (empty)
\r\n      // CRLF that marks the end of the headers

// Response body (empty)
```

For more information about HTTP responses, see the [MDN Web Docs on HTTP responses](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages#http_responses) or the [HTTP/1.1 specification](https://datatracker.ietf.org/doc/html/rfc9112#name-message).

## Tests

The tester will execute your program like this:
```
$ ./your_program.sh
```

The tester will then send an HTTP `GET` request to your server:
```
$ curl -v http://localhost:4221
```

Your server must respond to the request with the following response:
```
HTTP/1.1 200 OK\r\n\r\n
```

# Notes

- You can ignore the contents of the request. We'll cover parsing requests in later stages.
- This challenge uses HTTP/1.1.
- To learn how HTTP works, you'll implement your server from scratch using TCP primitives, without relying on built-in or external HTTP libraries.

## How to pass this stage

### 1. Write code to pass this stage

Head over to your editor / IDE and implement your solution.

If you want a quick look at what functions to use or how to structure your code, we recommend looking at [Code Examples](https://app.codecrafters.io/courses/http-server/stages/ia4/code-examples).

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
        - TODO
    - output:
        - TODO
    - side effects:
        - TODO
    - questions
        - HTTP core concepts + basics?
            - TODO
        - socket programming core concepts + basics?
            - TODO
        - Python `socket` built-in module useful classes / methods / functions?
            - TODO
        - HTTP Response message is sent to HTTP client encoded as bytes?
    - notes
        - use HTTP version 1.1
            - messages are text-based (i.e., not binary-encoded)
        - send a HTTP Response status line to the sender client
- PEDAC: Examples
    - ex.1
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
    - TODO