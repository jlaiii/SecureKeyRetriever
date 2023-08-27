from http.server import BaseHTTPRequestHandler, HTTPServer

class KeyServerHandler(BaseHTTPRequestHandler):

    def _set_response(self, content_type="text/html"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self._set_response()
            response = "<html><body>"

            keys = self._read_keys_from_file()

            if len(keys) > 0:
                key = keys[0]
                response += f"<p>Keys in stock: {len(keys)}</p>"
                response += f"<p>Next key available: {key}</p>"
                response += f'<form method="post" action="/get_key">'
                response += f'<input type="hidden" name="key" value="{key}">'
                response += f'<input type="submit" value="Get Another Key">'
                response += f'</form>'
            else:
                response += "<p>No keys available.</p>"

            response += "</body></html>"
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Page not found.".encode())

    def do_POST(self):
        if self.path == "/get_key":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            key = post_data.split("=")[1]

            keys = self._read_keys_from_file()

            if key in keys:
                keys.remove(key)  # Remove the key from the list
                self._save_keys_to_file(keys)  # Save the updated keys to file

            self.send_response(301)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Page not found.".encode())

    def _read_keys_from_file(self):
        with open("keys.txt", "r") as f:
            return [key.strip() for key in f.readlines()]

    def _save_keys_to_file(self, keys):
        with open("keys.txt", "w") as f:
            f.write("\n".join(keys))

def run():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, KeyServerHandler)
    print("Server started on port 8000")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
