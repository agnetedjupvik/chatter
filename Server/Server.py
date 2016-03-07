# -*- coding: utf-8 -*-
import SocketServer
import json
import time
import re

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

users = {}

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        print "New Handler Created"
        # Loop that listens for messages from the client
        while True:
            try:
                received_string = self.connection.recv(4096)
                message = json.loads(received_string)
                request = message["request"].lower()
                content = message["content"]
                response = {}
                print "Message Received"
                if request == 'login':
                    response["timestamp"] = str(time.time()*1000)
                    response["sender"] = "Server"
                    if self.validate_user_name(content):
                        users[self] = content
                        response["response"] = "Info"
                        response["content"] = "Login Successful"
                    else:
                        response["response"] = "Error"
                        response["content"] = "Username Taken"
                    self.connection.send(json.dumps(response))
                elif request == 'logout' and self.is_logged_in():
                    del users[self]
                    return
                elif request == "msg" and self.is_logged_in():
                    self.connection.send("Ok Command")
                    pass
                elif request == "names" and self.is_logged_in():
                    response["timestamp"] = str(time.time()*1000)
                    response["sender"] = "Server"
                    response["response"] = "Info"
                    response["content"] = users.values()
                    self.connection.send(json.dumps(response))
                    pass
                elif request == "help":
                    self.connection.send("Ok Command")
                    pass
                else:
                    response["timestamp"] = str(time.time()*1000)
                    response["sender"] = "Server"
                    response["response"] = "Error"
                    response["content"] = "Invalid Command"
                    self.connection.send(json.dumps(response))
                    pass;
            except:
                pass

    # Validate user name!
    def validate_user_name(self, username):
        if username in users.values():
            return False
        if re.match("^[A-Za-z0-9_-]*", username):
            print "Regex Match"
            return True
        print "No Match"
        return False

    def is_logged_in(self):
        print "Checking logged in status..."
        if self in users.keys():
            print "OK"
            return True
        print "Not ok"
        response = {}
        response["timestamp"] = str(time.time()*1000)
        response["sender"] = "Server"
        response["response"] = "Error"
        response["content"] = "You are not logged in."
        self.connection.send(json.dumps(response))
        return False



class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
