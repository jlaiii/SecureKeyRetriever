from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import random
import string

UPLOAD_DIRECTORY = "keypages"
LINK_LENGTH = random.randint(2, 4)  # Random length
GENERATED_KEYS_FILE = "generated_keys.txt"
KEYS_GIVEN_OUT_FILE = os.path.join(UPLOAD_DIRECTORY, "keys_given_out.txt")  # File to store keys given out
KEYS_GIVEN_OUT = 0

def generate_random_link(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_and_remove_key():
    global KEYS_GIVEN_OUT

    with open(GENERATED_KEYS_FILE, "r") as file:
        keys = file.readlines()

    if keys:
        key = keys[0].strip()
        with open(GENERATED_KEYS_FILE, "w") as file:
            file.writelines(keys[1:])
        KEYS_GIVEN_OUT += 1
        with open(KEYS_GIVEN_OUT_FILE, "w") as count_file:
            count_file.write(str(KEYS_GIVEN_OUT))  # Update the count in the file
        return key
    else:
        return None

class KeyServerHandler(BaseHTTPRequestHandler):

    def _set_response(self, content_type="text/html"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        global KEYS_GIVEN_OUT

        if self.path == "/":
            self._set_response()
            num_keys = len(open(GENERATED_KEYS_FILE).readlines())
            response = f"<html><body>"
            response += "<h1>Welcome to the WARP+ Key Generator</h1>"
            response += f"<p>Keys in stock: {num_keys}</p>"
            response += f"<p>Keys given out: {KEYS_GIVEN_OUT}</p>"
            response += '<form method="post" action="/get_key">'
            response += '<input type="submit" value="Get Key">'
            response += '</form>'
            response += "</body></html>"
            self.wfile.write(response.encode())
        elif self.path.startswith("/keys/"):
            page_path = os.path.join(UPLOAD_DIRECTORY, os.path.basename(self.path))
            if os.path.exists(page_path):
                self._set_response()
                with open(page_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Page not found.")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Page not found.")

    def do_POST(self):
        if self.path == "/get_key":
            self._set_response()
            key = get_and_remove_key()
            if key:
                while True:
                    page_link = generate_random_link(LINK_LENGTH)
                    page_filename = os.path.join(UPLOAD_DIRECTORY, page_link + ".html")
                    if not os.path.exists(page_filename):
                        break
                with open(page_filename, 'w') as html_file:
                    html_file.write(f"<html><body><h1>Your Key</h1><p>{key}</p>")
                    html_file.write('<a href="/">Home</a>')
                    html_file.write("</body></html>")
                response = """
                <html>
                <head>
                <title>Redirecting...</title>
                <script>
                setTimeout(function() {
                    window.location.href = '/keys/""" + page_link + """.html';
                }, 2000);
                </script>
                </head>
                <body>
                <p>You will be redirected to your key page shortly...</p>
                </body>
                </html>
                """
                self.wfile.write(response.encode())
            else:
                self.wfile.write("No keys available.".encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Page not found.".encode())

def load_keys_given_out():
    global KEYS_GIVEN_OUT
    if os.path.exists(KEYS_GIVEN_OUT_FILE):
        with open(KEYS_GIVEN_OUT_FILE, "r") as count_file:
            try:
                KEYS_GIVEN_OUT = int(count_file.read())  # Load the count from the file
            except ValueError:
                pass

def run():
    load_keys_given_out()  # Load keys given out count
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, KeyServerHandler)
    print("Server started on port 8000")
    httpd.serve_forever()

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    if not os.path.exists(GENERATED_KEYS_FILE):
        open(GENERATED_KEYS_FILE, "w").close()
    run()
