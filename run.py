import functools

from dotenv import load_dotenv
import uvicorn
import http.server
import socketserver
import threading
import os

load_dotenv()


def run_static_server():
	directory = os.path.join(os.path.dirname(__file__), "src", "website")
	handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
	with socketserver.TCPServer(("", 8080), handler) as httpd:
		print("Serving static website at http://127.0.0.1:8080")
		httpd.serve_forever()


if __name__ == "__main__":
	static_thread = threading.Thread(target=run_static_server, daemon=True)
	static_thread.start()

	uvicorn.run(
		"src.api.main:app",
		host="127.0.0.1",
		port=8000,
		reload=True
	)
