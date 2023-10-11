from http.server import HTTPServer, CGIHTTPRequestHandler


server = HTTPServer(("localhost", 20201), CGIHTTPRequestHandler)

print("----- Server started ------")

server.serve_forever()
