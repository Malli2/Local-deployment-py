import json, os, sys, threading, unittest
from urllib.request import urlopen
from http.server import ThreadingHTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
from app import Handler

class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_root(self):
        with urlopen(self.base + "/") as r:
            data = json.loads(r.read())
            self.assertEqual(r.status, 200)
            self.assertEqual(data["application"], "MTS Deployment Platform")

    def test_health(self):
        with urlopen(self.base + "/health") as r:
            self.assertEqual(json.loads(r.read())["status"], "healthy")

    def test_status(self):
        with urlopen(self.base + "/api/v1/status") as r:
            self.assertEqual(json.loads(r.read())["status"], "running")

if __name__ == "__main__":
    unittest.main()
