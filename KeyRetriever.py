from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi
import urllib.parse
import uuid
import random
import string

UPLOAD_DIRECTORY = "keypages"
LINK_LENGTH = 8
GENERATED_KEYS_FILE = "generated_keys.txt"

def generate_random_link(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_and_remove_key():
    with open(GENERATED_KEYS_FILE, "r") as file:
        keys = file.readlines()
    
    if keys:
        key = keys[0].strip()  # Get the first key and remove leading/trailing whitespaces
        with open(GENERATED_KEYS_FILE, "w") as file:
            file.writelines(keys[1:])  # Write back the remaining keys (excluding the first one)
        return key
    else:
        return None

class KeyServerHandler(BaseHTTPRequestHandler):

    def _set_response(self, content_type="text/html"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self._set_response()
            num_keys = len(open(GENERATED_KEYS_FILE).readlines())
            response = f"<html><body>"
            response += "<h1>Welcome to the Key Generator</h1>"
            response += f"<p>This is a 1.1.1.1 Key Generator. Keys in stock: {num_keys}</p>"
            response += '<form method="post" action="/get_key">'
            response += '<input type="submit" value="Get Key">'
            response += '</form>'
            response += "</body></html>"
            self.wfile.write(response.encode())
        elif self.path.startswith("/uploads/"):
            # Serve the generated HTML pages from the uploads directory
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
            
            # Get and remove a key from the list
            key = get_and_remove_key()
            
            if key:
                # Generate a unique HTML page filename
                page_link = generate_random_link(LINK_LENGTH)
                page_filename = os.path.join(UPLOAD_DIRECTORY, page_link + ".html")
                
                # Create the HTML page with the retrieved key
                with open(page_filename, 'w') as html_file:
                    html_file.write(f"<html><body><h1>Your Key</h1><p>{key}</p>")
                    html_file.write('<a href="/">Home</a>')  # Add the Home button
                    html_file.write("</body></html>")
                
                # Send the response with JavaScript for the delay
                response = """
                <html>
                <head>
                <title>Redirecting...</title>
                <script>
                setTimeout(function() {
                    window.location.href = '/uploads/""" + page_link + """.html';
                }, 2000); // 2-second delay
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

def run():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, KeyServerHandler)
    print("Server started on port 8000")
    httpd.serve_forever()

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    if not os.path.exists(GENERATED_KEYS_FILE):
        open(GENERATED_KEYS_FILE, "w").close()  # Create the keys file if it doesn't exist
    run()
