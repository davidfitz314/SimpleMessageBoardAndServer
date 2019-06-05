from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from pathlib import Path

memory = []

form = Path('MessageScreen.html').read_text()

class MessageServer(BaseHTTPRequestHandler):

    ##
    ## Sends the message data for the http headers and content,
    ## Sends a response 200 for when the data is posted.
    ##
    def do_POST(self):
        # Grabs the length of message content, no content defaults to 0
        length = int(self.headers.get('Content-Length', 0))
        # read the data from the request, amount based off of 'length'
        data = self.rfile.read(length).decode()
        # extract the message field from the request data
        message = parse_qs(data)["message"][0]
        print(message)
        # Escape HTML tags in the message so users can't break world+dog.
        message = message.replace("<", "&lt;")
        # Store the message in memory
        memory.append(message)
        # redirect via 303
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        # put the response together from the form and stored Messages
        mesg = form.format("\n".join(memory))
        self.wfile.write(mesg.encode())



##
## Grabs the address and port to use for the server,
## connects it with the server class for handling messages 'MessageServer',
## then launches the built in python server while running the 'MessageServer' methods for handling requests.
##
if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MessageServer)
    httpd.serve_forever()
