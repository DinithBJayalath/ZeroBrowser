import socket
import ssl

class URL:

    def __init__(self, url:str) -> None:
        self.scheme, url = url.split("://", 1) # Multiple assignment
        assert self.scheme in ["http", "https"]
        if "/" not in url: # This is to make sure that the url will always split into 2 parts
            url = url + "/"
        self.host, url = url.split("/", 1) # Multiple assignment
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port: int = int(port)
        elif self.scheme == "http":
            self.port: int = 80
        elif self.scheme == "https":
            self.port: int = 443
        self.path = "/" + url

    def request(self) -> str:
        s: socket.socket = socket.socket(
            family= socket.AF_INET,
            type= socket.SOCK_STREAM,
            proto= socket.IPPROTO_TCP,
        )
        s.connect((self.host, self.port))
        if self.scheme == "https":
            # This context wrapper is used to wrap the socket to encrypt the connection
            context = ssl.create_default_context()
            s = context.wrap_socket(s, server_hostname=self.host)
        # The next 3 lines of the code is the request, "\r\n" is to send the extra line to end the request in http
        request: str = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"
        s.send(request.encode("utf-8"))
        # makefile method waits for the whole response to come and make a file like structure
        #"r" is to denote reading
        # Response comes encoded so it needs to be decoded
        response = s.makefile("r", encoding="utf-8", newline="\r\n")
        status_line: str = response.readline()
        version, code, description = status_line.split(" ", 2)
        response_headers: dict = {}
        # The loop is to go through all the header lines
        while True:
            line: str = response.readline()
            if line == "\r\n": break # End of the response is denoted by the special new line
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip() # casefold method makes all the letters lowercase (HTTP headers are case-insensitive)
        # These 2 headers say if the data of the response is sent in and unusual way
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
        # Rest of the response is the body, which is the web page
        content: str = response.read()
        s.close()
        return content