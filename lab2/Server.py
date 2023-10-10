from common.servers.CGIServer import CGIServer


def main():
    server = CGIServer(path="localhost", port=20200)


if __name__ == '__main__':
    main()
