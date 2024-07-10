# Create HTTP Server 

### Setting Up an HTTP Server with CRUD Operations in Python

1. **Import Required Modules**:
   - Use `http.server`, `socketserver`, `os`, `urllib.parse`, and `csv` modules.

2. **Define a Custom Request Handler**:
   - Subclass `http.server.BaseHTTPRequestHandler` to handle GET and POST requests.

3. **Handle GET Requests**:
   - Serve `index.html` for `/` path.
   - Serve `style.css` for `/style.css` path.
   - Return 404 for other paths.

4. **Handle POST Requests**:
   - Parse form data (`mail` and `password`) from the request.
   - Save data to a CSV file (`users.csv`).
   - Respond with a confirmation message in HTML format.

5. **Serve Static Files**:
   - Implement `_serve_static_file` method to read and serve static files (`index.html` and `style.css`).

6. **Save Data to CSV**:
   - Implement `_save_to_csv` method to append form data (`mail` and `password`) to `users.csv`.

7. **Run the HTTP Server**:
   - Set up `socketserver.TCPServer` to listen on a specified port (`8000`).
   - Use `os.chdir()` to navigate to the directory containing static files.
   - Start the server with `httpd.serve_forever()`.

### Example Code:

Here’s a concise example based on the above steps:

```python
import http.server
import socketserver
import os
import csv
from urllib.parse import urlparse, parse_qs

class CRUDRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/':
            self._serve_static_file('index.html', 'text/html')
        elif path == '/style.css':
            self._serve_static_file('style.css', 'text/css')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        parsed_qs = parse_qs(post_data)
        mail = parsed_qs.get('mail', [''])[0]
        password = parsed_qs.get('password', [''])[0]
        
        self._save_to_csv(mail, password)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>Form Submitted Successfully!</h1></body></html>')

    def _serve_static_file(self, filename, content_type):
        try:
            with open(filename, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(file.read())
        except IOError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def _save_to_csv(self, mail, password):
        with open('users.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([mail, password])

if __name__ == '__main__':
    PORT = 8000
    
    os.chdir('/path/to/static/files')  # Replace with your directory path
    
    handler = CRUDRequestHandler
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Server running on port {PORT}")
        httpd.serve_forever()
```

### Usage:

1. **Setup**:
   - Save the above code in a file named `http_server.py`.
   - Create `index.html` and `style.css` files in the same directory as the script.

2. **Run the Server**:
   - Open a terminal or command prompt.
   - Navigate to the directory containing `http_server.py` and the static files.
   - Run the server with `python http_server.py`.

3. **Access the Server**:
   - Open a web browser and go to `http://localhost:8000/`.
   - Fill out the form in `index.html` and submit it to save data to `users.csv`.

### Notes:

- **Security**: Implement input validation and security measures before deploying in a production environment.
- **Expansion**: Extend the server by adding PUT and DELETE methods for complete CRUD functionality.
- **Error Handling**: Enhance error handling for robustness and reliability.

--- 