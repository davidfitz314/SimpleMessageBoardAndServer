# The server should be listening on port 8000, answer a GET request with
# an HTML document, and answer a POST request with a redirect to the
# main page.

import requests, random, socket

def test_connect():
    '''Connecting to Localhost 8000 Server'''
    print("Testing Server Connection.")
    try:
        with socket.socket() as s:
           s.connect(("localhost", 8000))
        print("Connection succeeded!")
        return None
    except socket.error:
        return "No Server Connection Found"

def test_POST_303():
    '''The server should accept a POST and return a 303 to /.'''
    print("Testing POST request and watching for a redirect request.")
    mesg = random.choice(["Hello World", "Bonjour", "Hola", "Hey...HEY...heeeey"])
    uri = "http://localhost:8000/"
    try:
        r = requests.post(uri, data = {'message': mesg}, allow_redirects=False)
    except requests.RequestException as e:
        return ("Server Communication Error. ({})\n").format(e)
    if r.status_code == 501:
        return ("Post status code 501 Not Implemented.\n")
    elif r.status_code != 303:
        return ("Post status code {} instead of a 303 redirect.").format(r.status_code)
    elif r.headers['location'] != '/':
        return ("303 redirect location is invalid."
                "expected '/' but sent '{}'.").format(
                    r.headers['location'])
    else:
        print("POST request succeeded.")
        return None

def test_GET():
    '''Server use GET and return the form.'''
    print("Testing GET request.")
    uri = "http://localhost:8000/"
    try:
        r = requests.get(uri)
    except requests.RequestException as e:
        return ("Server Communication Error. ({})\n").format(e)
    if r.status_code == 501:
        return ("GET status code 501, Not Implemented.\n")
    elif r.status_code != 200:
        return ("GET status code {} instead of a 200 OK."
                ).format(r.status_code)
    elif not r.headers['content-type'].lower().startswith('text/html'):
        return ("Headers Content-type: not text/html.")
    elif '<title>Current Messages</title>' not in r.text:
        return ("Invalid Form Returned.")
    else:
        print("GET request succeeded!")
        return None

def test_memory():
    '''Server Memory Test.'''
    print("Testing Saving Messages with Server.")
    uri = "http://localhost:8000"
    mesg = random.choice(["Dog", "Cat", "Horse"])
    r = requests.post(uri, data = {'message': mesg})
    if r.status_code != 200:
        return ("Invalid status code {} Requires 200 on Post-Redirect-Get."
                ).format(r.status_code)
    elif mesg not in r.text:
        return ("No New Messages displayed.\n"
                "Expected '{}', returned\n"
                "{}").format(mesg, r.text)
    else:
        print("Post-Redirect-Get succeeded!")

if __name__ == '__main__':
    tests = [test_connect, test_POST_303, test_GET, test_memory]
    for test in tests:
        problem = test()
        if problem is not None:
            print(problem)
            break
    if not problem:
        print("All tests succeeded!")
