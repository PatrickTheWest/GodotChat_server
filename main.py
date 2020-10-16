import ws_server


def main():
    print("Starting websockets server...")
    ws_server.run_server(8080)


if __name__ == '__main__':
    main()


