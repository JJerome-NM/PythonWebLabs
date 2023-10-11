from os import scandir
from http.server import HTTPServer, CGIHTTPRequestHandler
from threading import Thread


class CGIServer(Thread):

    def __init__(self, path: str = "localhost", port: int = 20200, cgi_bin_path: str = "cgi-bin"):
        super().__init__(daemon=True)
        print("Staring server...")

        self._cgi_bin_path = cgi_bin_path

        self._server = HTTPServer((path, port), CGIHTTPRequestHandler)
        self.base_url = f"http://{path}:{port}"

        print(f"----- Server started on {self.base_url} ------")

        print("There are such links as:")
        self.show_cgi_urls(cgi_bin_path)

    def run(self):
        self._server.serve_forever()

    def show_cgi_urls(self, dir_path: str = "cgi-bin"):
        for entity in scandir(dir_path):
            if entity.is_dir():
                self.show_cgi_urls(entity.path)
            else:
                print(f"{self.base_url}/{entity.path.replace("\\", "/")}")


if __name__ == '__main__':
    server = CGIServer()
