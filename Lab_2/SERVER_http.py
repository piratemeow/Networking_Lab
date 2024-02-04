import http.server
import socketserver
import threading
import mimetypes
import os

PORT = 8080
DIRECTORY = "/home/student/Screenshots"  # Change this to the directory containing your files

class MultiThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

class FileRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Set the directory to the specified path
        self.directory = DIRECTORY

        # Call the parent class method to handle regular GET requests
        if not self.translate_path(self.path):
            super().do_GET()
            return

        # Handle file download requests
        file_path = os.path.join(self.directory, self.path)
        print(f"downloading....{file_path}")
        print()
        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
            self.send_header('Content-Length', os.path.getsize(file_path))
            self.end_headers()

            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html/image/video')
            self.end_headers()
            self.wfile.write(b'File not found')

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            uploaded_file = self.rfile.read(content_length)

            filename = self.headers.get('filename', 'uploaded_file')
            file_path = os.path.join(DIRECTORY, filename)

            # Ensure the directory exists before writing the file
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            print("uploading...")

            with open(file_path, 'wb') as file:
                file.write(uploaded_file)

            # Extract file extension from the filename
            _, file_extension = os.path.splitext(filename)

            # Set the appropriate content type based on the file extension
            content_type, _ = mimetypes.guess_type(file_extension, strict=False)
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()

            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
            print("Upload sucessfull")


        except Exception as e:
            print(f"Error uploading file: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Internal Server Error')
def start_server():
    handler = FileRequestHandler
    httpd = MultiThreadedHTTPServer(("", PORT), handler)
    print(f"Server is listening on port {PORT}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer is shutting down.")
        httpd.shutdown()


# Create the 'files' directory if it doesn't exist
os.makedirs(DIRECTORY, exist_ok=True)

# Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.start()
server_thread.join()
