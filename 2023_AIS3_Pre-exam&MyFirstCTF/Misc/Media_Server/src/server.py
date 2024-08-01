from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from functools import lru_cache
import re
import os
import mimetypes


@lru_cache(maxsize=1024)
def cached_size(filepath):
    return os.path.getsize(filepath)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if re.fullmatch(r"/media/[a-zA-Z0-9.]+", self.path):
            return self.do_media()

        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            with open("index.html", "rb") as f:
                self.wfile.write(f.read())
        elif self.path == secret_path:
            with os.popen("/readflag", "r") as f:
                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(f.read().encode())
        else:
            self.send_error(404)

    def do_media(self):
        filepath = self.path[1:]
        if os.path.exists(filepath):
            filesize = cached_size(filepath)

            range_hdr = self.headers.get("Range", "")
            is_range_request = False
            if range_hdr.startswith("bytes="):
                range_hdr = range_hdr[6:]
                range_start, range_end = range_hdr.split("-")
                range_start = int(range_start) if range_start else 0
                range_end = int(range_end) if range_end else filesize - 1
                is_range_request = True

            typ, _ = mimetypes.guess_type(filepath)
            self.send_response(206 if is_range_request else 200)
            self.send_header("Content-type", typ)
            with open(filepath, "rb") as f:
                self.send_header("Accept-Ranges", "bytes")
                if is_range_request:
                    f.seek(range_start)
                    size = range_end - range_start + 1
                    self.send_header("Content-Length", str(size))
                    self.send_header(
                        "Content-Range",
                        f"bytes {range_start}-{range_end}/{filesize}",
                    )
                    self.end_headers()
                    self.wfile.write(f.read(size))
                else:
                    self.send_header("Content-Length", str(filesize))
                    self.end_headers()
                    self.wfile.write(f.read())
        else:
            self.send_error(404)


if __name__ == "__main__":
    secret_path = "/flag_" + os.urandom(16).hex()
    print(secret_path)
    server = ThreadingHTTPServer(("", 8000), RequestHandler)
    print("Starting server, use <Ctrl-C> to stop")
    server.serve_forever()
