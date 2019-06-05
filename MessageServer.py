from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

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
        # Send the message field back as the response
        self.send_response(200)
        # message response data should be text and use utf-8
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_headers()
        # write the message and make sure it is encoded to correct type
        self.wfile.write(message.encode())

    ##
    ## 
    ##
    ##
    def do_GET(self):



##
## Grabs the address and port to use for the server,
## connects it with the server class for handling messages 'MessageServer',
## then launches the built in python server while running the 'MessageServer' methods for handling requests.
##
if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MessageServer)
    httpd.serve_forever()
