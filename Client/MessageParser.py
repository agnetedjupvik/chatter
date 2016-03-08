import json

class MessageParser():
    def __init__(self):
        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'msg': self.parse_msg,
            'history': self.parse_history
        }

    def parse(self, payload):
        payload = json.loads(payload) # decode the JSON object


        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            pass
            # Response not valid

    def parse_msg(self, payload):
        message = payload['content']
        username = payload['sender']
        result = username + ": " + message
        return result

    def parse_error(self, payload):
        error = payload['content']
        return "There were an error: " + error

    def parse_info(self, payload):
        info = payload['content']
        result = "Here's some information: " + info
        return result

    def parse_history(self, payload):
        history = payload['content']
        return "Message: " + history
