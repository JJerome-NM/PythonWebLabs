from http.server import HTTPServer, CGIHTTPRequestHandler


class CGIServer:

    def __init__(self, path: str = "localhost", port: int = 20200):
        print("Staring server...")

        self._server = HTTPServer((path, port), CGIHTTPRequestHandler)

        print(f"----- Server started on http://{path}:{port} ------")

        self._server.serve_forever()


if __name__ == '__main__':
    server = CGIServer()
