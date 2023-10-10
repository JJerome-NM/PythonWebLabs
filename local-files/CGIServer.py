from http.server import HTTPServer, CGIHTTPRequestHandler


server = HTTPServer(("localhost", 20200), CGIHTTPRequestHandler)

print("----- Server started ------")

server.serve_forever()
