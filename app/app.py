import json, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

APP_NAME = os.getenv("APP_NAME", "MTS Deployment Platform")
APP_VERSION = os.getenv("APP_VERSION", "dev")
APP_ENV = os.getenv("APP_ENV", "local")

class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "healthy"})
        elif self.path == "/api/v1/status":
            self.send_json(200, {"application": APP_NAME, "version": APP_VERSION,
                                 "environment": APP_ENV, "status": "running",
                                 "platform": "Kubernetes" if APP_ENV == "kubernetes" else "local"})
        elif self.path == "/":
            self.send_json(200, {"application": APP_NAME,
                                 "message": "Hello from your local Kubernetes deployment!",
                                 "version": APP_VERSION, "health": "/health",
                                 "status_endpoint": "/api/v1/status"})
        else:
            self.send_json(404, {"error": "not_found", "path": self.path})

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}", flush=True)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    print(f"Starting {APP_NAME} on 0.0.0.0:{port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
