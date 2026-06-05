import os
import socket

from app import create_app

app = create_app()


def pick_port(default_port=5000, max_port=5010):
    requested_port = int(os.getenv("PORT", default_port))

    for port in range(requested_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port

    return requested_port

if __name__ == "__main__":
    port = pick_port()
    print(f"Starting Flask on port {port}")
    app.run(debug=True, port=port)
