import json

class MessageParser():
    def __init__(self):
        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'msg': self.parse,
            'history': self.parse_history
        }

    def parse(self, payload):
        payload = json.loads(payload) # decode the JSON object


        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            pass
            # Response not valid

    def parse_error(self, payload):
        error = payload['content']
        return "There were an error: " + error

    def parse_info(self, payload):
        info = payload['content']
        return "Here's some information: " + info

    def parse_history(self, payload):
        msg = payload['content']
        return "Message: " + msg
    # Include more methods for handling the different responses...
